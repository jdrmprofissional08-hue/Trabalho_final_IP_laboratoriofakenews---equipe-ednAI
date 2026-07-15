# -*- coding: utf-8 -*-

import logging
import random
import hmac
import secrets
import sqlite3
import sys
from pathlib import Path

from flask import Flask, jsonify, render_template, request, send_from_directory
from werkzeug.exceptions import HTTPException

PROJECT_DIR = Path(__file__).resolve().parent.parent
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

try:
    from backend.database import BASE_DIR, get_connection, init_db, row_to_dict
except ModuleNotFoundError:
    from database import BASE_DIR, get_connection, init_db, row_to_dict

from app.ai import EdnaiAgent
from app.ai.gemini_client import GeminiConfigurationError

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger("ednai.backend")

app = Flask(
    __name__,
    template_folder=str(PROJECT_DIR / "web" / "templates"),
    static_folder=str(PROJECT_DIR / "web" / "static"),
    static_url_path="/static",
)
init_db()
ednai_agent = EdnaiAgent()


def normalize_theme(value):
    mapping = {
        "saude": "Ciência",
        "saúde": "Ciência",
        "ciencia": "Ciência",
        "ciência": "Ciência",
        "tecnologia": "Tecnologia",
        "esportes": "Esportes",
        "cinema": "Cinema",
    }
    text = str(value).strip()
    return mapping.get(text.lower(), text)


def parse_int(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def parse_bool(value, default=False):
    if isinstance(value, bool):
        return value
    if isinstance(value, int):
        return value != 0
    if isinstance(value, str):
        text = value.strip().lower()
        if text in {"true", "1", "sim", "s", "yes", "y"}:
            return True
        if text in {"false", "0", "nao", "não", "n", "no"}:
            return False
    return default


def get_json_payload():
    data = request.get_json(silent=True)
    return data if isinstance(data, dict) else {}


def get_request_token(data=None):
    data = data if isinstance(data, dict) else {}
    return str(
        request.headers.get("X-Partida-Token")
        or data.get("token")
        or ""
    ).strip()


def parse_web_answer(value):
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        text = value.strip().lower()
        if text in {"true", "fato"}:
            return True
        if text in {"false", "fake"}:
            return False
    return None


def news_payload(row):
    item = row_to_dict(row)
    item["is_fato"] = bool(item["is_fato"])
    item["image_path"] = str((BASE_DIR / item["image_path"]).resolve())
    item["image_url"] = f"{request.host_url.rstrip('/')}/api/imagens/{Path(item['image_path']).name}"
    return item


def public_news_payload(row):
    item = row_to_dict(row)
    image_name = Path(item.get("image_path", "")).name
    return {
        "id": item["id"],
        "tema": item["tema"],
        "manchete": item["manchete"],
        "texto": item["texto"],
        "fonte": item["fonte"],
        "tempo": item["tempo"],
        "fonte_url": item["fonte_url"],
        "image_url": f"/api/imagens/{image_name}" if image_name else "",
    }


def validate_name(nome):
    nome = str(nome or "").strip()
    if len(nome) < 3 or len(nome) > 80:
        return ""
    return nome


def validate_age(idade):
    idade = parse_int(idade, 0)
    if idade < 1 or idade > 120:
        return 0
    return idade


def get_available_themes():
    with get_connection() as conn:
        rows = conn.execute("SELECT DISTINCT tema FROM noticias ORDER BY tema").fetchall()
    return [row["tema"] for row in rows]


def normalize_themes(themes):
    if isinstance(themes, str):
        raw_themes = themes.split(",")
    elif isinstance(themes, list):
        raw_themes = themes
    else:
        raw_themes = []

    available = set(get_available_themes())
    normalized = []
    for theme in raw_themes:
        normalized_theme = normalize_theme(theme)
        if normalized_theme in available and normalized_theme not in normalized:
            normalized.append(normalized_theme)
    return normalized


def fetch_news_rows(themes=None, limit=10):
    themes = themes or []
    limit = max(1, min(parse_int(limit, 10), 40))

    with get_connection() as conn:
        if themes:
            placeholders = ",".join("?" for _ in themes)
            rows = conn.execute(
                f"SELECT * FROM noticias WHERE tema IN ({placeholders})",
                themes,
            ).fetchall()
        else:
            rows = conn.execute("SELECT * FROM noticias").fetchall()

    items = list(rows)
    random.shuffle(items)
    return items[:limit]


def insert_user(conn, nome, idade, consentimento):
    cursor = conn.execute(
        "INSERT INTO usuarios (nome, idade, consentimento) VALUES (?, ?, ?)",
        (nome, idade, int(consentimento)),
    )
    return cursor.lastrowid


def create_user_record(nome, idade, consentimento):
    with get_connection() as conn:
        return insert_user(conn, nome, idade, consentimento)


def insert_match(conn, usuario_id, temas, total_questoes, token_web=None):
    cursor = conn.execute(
        """
        INSERT INTO partidas (usuario_id, temas, total_questoes, token_web)
        VALUES (?, ?, ?, ?)
        """,
        (usuario_id, temas, total_questoes, token_web),
    )
    return cursor.lastrowid


def create_match_record(usuario_id, temas, total_questoes, token_web=None):
    with get_connection() as conn:
        return insert_match(conn, usuario_id, temas, total_questoes, token_web)


def create_web_match_record(nome, idade, consentimento, themes, rows):
    token = secrets.token_urlsafe(32)
    with get_connection() as conn:
        conn.execute("BEGIN IMMEDIATE")
        usuario_id = insert_user(conn, nome, idade, consentimento)
        partida_id = insert_match(conn, usuario_id, ",".join(themes), len(rows), token)
        conn.executemany(
            """
            INSERT INTO partida_noticias (partida_id, noticia_id, ordem)
            VALUES (?, ?, ?)
            """,
            [
                (partida_id, row["id"], index)
                for index, row in enumerate(rows)
            ],
        )
    return usuario_id, partida_id, token


def get_match(match_id):
    with get_connection() as conn:
        return conn.execute(
            """
            SELECT partidas.*, usuarios.nome, usuarios.consentimento
              FROM partidas
              JOIN usuarios ON usuarios.id = partidas.usuario_id
             WHERE partidas.id = ?
            """,
            (match_id,),
        ).fetchone()


def get_web_match_or_error(match_id, token):
    if not token:
        return None, json_error("Token da partida obrigatório.", 403)

    match = get_match(match_id)
    if not match:
        return None, json_error("Partida não encontrada.", 404)

    stored_token = str(match["token_web"] or "")
    if not stored_token or not hmac.compare_digest(stored_token, token):
        logger.warning("Token inválido para partida web: partida_id=%s", match_id)
        return None, json_error("Partida inválida ou expirada. Reinicie a atividade.", 403)

    return match, None


def get_web_question(match_id, index):
    with get_connection() as conn:
        row = conn.execute(
            """
            SELECT noticias.*
              FROM partida_noticias
              JOIN noticias ON noticias.id = partida_noticias.noticia_id
             WHERE partida_noticias.partida_id = ?
               AND partida_noticias.ordem = ?
            """,
            (match_id, index),
        ).fetchone()
        answered = None
        if row:
            answered = conn.execute(
                """
                SELECT id
                  FROM respostas
                 WHERE partida_id = ? AND noticia_id = ?
                 LIMIT 1
                """,
                (match_id, row["id"]),
            ).fetchone()
    if not row:
        return None
    item = public_news_payload(row)
    item["respondida"] = answered is not None
    return item


def get_match_result(match_id, include_items=False):
    match = get_match(match_id)
    if not match:
        return None

    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT respostas.resposta_jogador,
                   respostas.acertou,
                   noticias.id,
                   noticias.tema,
                   noticias.manchete,
                   noticias.texto,
                   noticias.is_fato,
                   noticias.explicacao,
                   noticias.fonte,
                   noticias.fonte_url
              FROM respostas
              JOIN noticias ON noticias.id = respostas.noticia_id
             WHERE respostas.partida_id = ?
             ORDER BY respostas.id ASC
            """,
            (match_id,),
        ).fetchall()

    correct = []
    mistakes = []
    for row in rows:
        item = {
            "id": row["id"],
            "tema": row["tema"],
            "manchete": row["manchete"],
            "texto": row["texto"],
            "resposta_jogador": bool(row["resposta_jogador"]),
            "is_fato": bool(row["is_fato"]),
            "explicacao": row["explicacao"],
            "fonte": row["fonte"],
            "fonte_url": row["fonte_url"],
        }
        if row["acertou"]:
            correct.append(item)
        else:
            mistakes.append(item)

    score = sum(1 for row in rows if row["acertou"])
    total = int(match["total_questoes"])
    result = {
        "partida_id": match_id,
        "nome": match["nome"],
        "score": score,
        "total": total,
        "erros": max(total - score, 0),
        "respondidas": len(rows),
        "duracao_segundos": int(match["duracao_segundos"]),
        "finalizada": bool(match["finalizada"]),
    }
    if include_items:
        result["mistakes"] = mistakes
        result["correct"] = correct
    return result


def calculate_match_score(match_id):
    with get_connection() as conn:
        row = conn.execute(
            "SELECT COUNT(*) AS acertos FROM respostas WHERE partida_id = ? AND acertou = 1",
            (match_id,),
        ).fetchone()
    return int(row["acertos"]) if row else 0


def record_web_answer(match_id, token, noticia_id, resposta_jogador):
    with get_connection() as conn:
        conn.execute("BEGIN IMMEDIATE")
        match = conn.execute(
            "SELECT * FROM partidas WHERE id = ?",
            (match_id,),
        ).fetchone()
        if not match:
            return None, json_error("Partida não encontrada.", 404)
        if match["finalizada"]:
            return None, json_error("Esta partida já foi finalizada.", 409)
        if not match["token_web"] or not hmac.compare_digest(str(match["token_web"]), token):
            logger.warning("Token inválido ao responder: partida_id=%s", match_id)
            return None, json_error("Partida inválida ou expirada. Reinicie a atividade.", 403)

        noticia = conn.execute(
            """
            SELECT noticias.*
              FROM partida_noticias
              JOIN noticias ON noticias.id = partida_noticias.noticia_id
             WHERE partida_noticias.partida_id = ?
               AND partida_noticias.noticia_id = ?
            """,
            (match_id, noticia_id),
        ).fetchone()
        if not noticia:
            return None, json_error("Esta notícia não pertence à partida.", 403)

        resposta_existente = conn.execute(
            """
            SELECT id
              FROM respostas
             WHERE partida_id = ? AND noticia_id = ?
             LIMIT 1
            """,
            (match_id, noticia_id),
        ).fetchone()
        if resposta_existente:
            return None, json_error("Esta questão já foi respondida.", 409)

        is_fato = bool(noticia["is_fato"])
        acertou = resposta_jogador == is_fato
        conn.execute(
            """
            INSERT INTO respostas (partida_id, noticia_id, resposta_jogador, acertou)
            VALUES (?, ?, ?, ?)
            """,
            (match_id, noticia_id, int(resposta_jogador), int(acertou)),
        )

        stats = conn.execute(
            """
            SELECT COUNT(*) AS respondidas,
                   SUM(CASE WHEN acertou = 1 THEN 1 ELSE 0 END) AS acertos
              FROM respostas
             WHERE partida_id = ?
            """,
            (match_id,),
        ).fetchone()

    return {
        "acertou": acertou,
        "resposta_jogador": resposta_jogador,
        "resposta_correta": is_fato,
        "explicacao": noticia["explicacao"],
        "fonte": noticia["fonte"],
        "fonte_url": noticia["fonte_url"],
        "acertos": int(stats["acertos"] or 0),
        "respondidas": int(stats["respondidas"] or 0),
        "total": int(match["total_questoes"]),
    }, None


def finalize_match_record(match_id, duracao_segundos, acertos=None, require_all_answers=False):
    with get_connection() as conn:
        conn.execute("BEGIN IMMEDIATE")
        match = conn.execute("SELECT * FROM partidas WHERE id = ?", (match_id,)).fetchone()
        if not match:
            return None, json_error("Partida não encontrada.", 404)

        stats = conn.execute(
            """
            SELECT COUNT(*) AS respondidas,
                   SUM(CASE WHEN acertou = 1 THEN 1 ELSE 0 END) AS acertos
              FROM respostas
             WHERE partida_id = ?
            """,
            (match_id,),
        ).fetchone()
        respondidas = int(stats["respondidas"] or 0)
        total = int(match["total_questoes"])
        if require_all_answers and respondidas < total:
            return None, json_error("Responda todas as questões antes de finalizar.", 400)

        final_score = parse_int(acertos, -1)
        if final_score < 0:
            final_score = int(stats["acertos"] or 0)

        conn.execute(
            """
            UPDATE partidas
               SET acertos = ?, duracao_segundos = ?, finalizada = 1
             WHERE id = ?
            """,
            (final_score, max(0, duracao_segundos), match_id),
        )

    return get_match_result(match_id), None


def json_error(message, status=400):
    return jsonify({"success": False, "message": message, "erro": message}), status


@app.errorhandler(Exception)
def handle_unexpected_error(error):
    if isinstance(error, HTTPException):
        return error
    logger.exception("Erro não tratado no backend")
    if request.path.startswith("/api/"):
        return json_error("Ocorreu um erro interno. Tente novamente.", 500)
    return render_template("erro.html", mensagem="Ocorreu um erro interno. Tente novamente."), 500


@app.get("/")
def pagina_inicial():
    return render_template("index.html")


@app.get("/quiz")
def pagina_quiz():
    return render_template("quiz.html")


@app.get("/resultado")
def pagina_resultado():
    return render_template("resultado.html")


@app.get("/ranking")
def pagina_ranking():
    return render_template("ranking.html")


@app.get("/api/health")
def health():
    return jsonify({"status": "ok"})


@app.get("/api/imagens/<path:filename>")
def serve_image(filename):
    safe_filename = Path(filename).name
    if safe_filename != filename:
        logger.warning("Tentativa inválida de acesso a imagem: %s", filename)
        return json_error("Imagem inválida.", 400)
    return send_from_directory(BASE_DIR / "news_images", safe_filename)


@app.get("/api/noticias")
def list_news():
    themes_param = request.args.get("temas", "")
    limit = max(1, min(parse_int(request.args.get("limite"), 10), 40))
    themes = [normalize_theme(theme) for theme in themes_param.split(",") if theme.strip()]

    rows = fetch_news_rows(themes, limit)
    return jsonify([news_payload(row) for row in rows])


@app.get("/api/noticias-web")
def list_public_news():
    themes = normalize_themes(request.args.get("temas", ""))
    limit = max(1, min(parse_int(request.args.get("limite"), 10), 40))
    rows = fetch_news_rows(themes, limit)
    return jsonify([public_news_payload(row) for row in rows])


@app.get("/api/temas")
def list_themes():
    return jsonify(get_available_themes())


@app.post("/api/usuarios")
def create_user():
    data = get_json_payload()
    nome = validate_name(data.get("nome", ""))
    idade = validate_age(data.get("idade"))
    consentimento = parse_bool(data.get("consentimento", True), True)

    if not nome or idade <= 0:
        return json_error("Dados de usuário inválidos.", 400)

    user_id = create_user_record(nome, idade, consentimento)

    return jsonify({"id": user_id, "nome": nome}), 201


@app.post("/api/partidas")
def create_match():
    data = get_json_payload()
    usuario_id = parse_int(data.get("usuario_id"), 0)
    temas = str(data.get("temas", ""))
    total_questoes = parse_int(data.get("total_questoes"), 0)

    if usuario_id <= 0 or total_questoes <= 0:
        return json_error("Dados de partida inválidos.", 400)

    match_id = create_match_record(usuario_id, temas, total_questoes)

    return jsonify({"id": match_id}), 201


@app.post("/api/web/partidas")
def create_web_match():
    data = get_json_payload()
    nome = validate_name(data.get("nome", ""))
    idade = validate_age(data.get("idade"))
    consentimento = parse_bool(data.get("consentimento", False), False)
    themes = normalize_themes(data.get("temas", []))
    limit = max(1, min(parse_int(data.get("total_questoes"), 10), 10))

    if not nome:
        return json_error("Informe um nome com pelo menos 3 caracteres.", 400)
    if idade <= 0:
        return json_error("Informe uma idade válida entre 1 e 120 anos.", 400)
    if not consentimento:
        return json_error("É necessário aceitar o termo de consentimento para iniciar.", 400)
    if not themes:
        return json_error("Selecione pelo menos um tema para iniciar a partida.", 400)

    rows = fetch_news_rows(themes, limit)
    if not rows:
        return json_error("Nenhuma notícia foi encontrada para os temas selecionados.", 404)

    usuario_id, partida_id, token = create_web_match_record(nome, idade, consentimento, themes, rows)
    logger.info("Partida web criada: partida_id=%s usuario_id=%s total=%s", partida_id, usuario_id, len(rows))

    return jsonify(
        {
            "success": True,
            "data": {
                "usuario_id": usuario_id,
                "partida_id": partida_id,
                "token": token,
                "total_questoes": len(rows),
            },
        }
    ), 201


@app.get("/api/partidas/<int:match_id>/questao")
def web_match_question(match_id):
    token = get_request_token()
    match, error_response = get_web_match_or_error(match_id, token)
    if error_response:
        return error_response

    index = parse_int(request.args.get("indice"), -1)
    total = int(match["total_questoes"])
    if index < 0 or index >= total:
        return json_error("Índice da questão inválido.", 400)

    question = get_web_question(match_id, index)
    if not question:
        return json_error("Questão não encontrada para esta partida.", 404)

    return jsonify(
        {
            "success": True,
            "data": {
                "questao": question,
                "indice": index,
                "total": total,
            },
        }
    )


@app.post("/api/partidas/<int:match_id>/respostas")
def create_answer(match_id):
    data = get_json_payload()
    noticia_id = parse_int(data.get("noticia_id"), 0)
    resposta_jogador = parse_bool(data.get("resposta_jogador", False), False)
    acertou = parse_bool(data.get("acertou", False), False)

    if noticia_id <= 0:
        return json_error("Notícia inválida.", 400)

    try:
        with get_connection() as conn:
            conn.execute(
                """
                INSERT INTO respostas (partida_id, noticia_id, resposta_jogador, acertou)
                VALUES (?, ?, ?, ?)
                """,
                (match_id, noticia_id, int(resposta_jogador), int(acertou)),
            )
    except sqlite3.IntegrityError:
        logger.info("Resposta duplicada ignorada no endpoint desktop: partida_id=%s noticia_id=%s", match_id, noticia_id)

    return jsonify({"status": "ok"}), 201


@app.post("/api/partidas/<int:match_id>/responder")
def answer_match_question(match_id):
    data = get_json_payload()
    noticia_id = parse_int(data.get("noticia_id"), 0)
    resposta_jogador = parse_web_answer(data.get("resposta_jogador"))
    token = get_request_token(data)

    if noticia_id <= 0:
        return json_error("Notícia inválida.", 400)
    if resposta_jogador is None:
        return json_error("Resposta inválida.", 400)
    if not token:
        return json_error("Token da partida obrigatório.", 403)

    data, error_response = record_web_answer(match_id, token, noticia_id, resposta_jogador)
    if error_response:
        return error_response

    return jsonify(
        {
            "success": True,
            "data": data,
        }
    ), 201


@app.post("/api/partidas/<int:match_id>/finalizar")
def finish_match(match_id):
    data = get_json_payload()
    acertos = parse_int(data.get("acertos"), -1)
    duracao_segundos = parse_int(data.get("duracao_segundos"), 0)

    result, error_response = finalize_match_record(
        match_id=match_id,
        duracao_segundos=duracao_segundos,
        acertos=acertos,
        require_all_answers=False,
    )
    if error_response:
        return error_response

    return jsonify({"status": "ok", "success": True, "data": result})


@app.post("/api/web/partidas/<int:match_id>/finalizar")
def finish_web_match(match_id):
    data = get_json_payload()
    token = get_request_token(data)
    match, error_response = get_web_match_or_error(match_id, token)
    if error_response:
        return error_response
    if match["finalizada"]:
        return jsonify({"status": "ok", "success": True, "data": get_match_result(match_id)})

    result, error_response = finalize_match_record(
        match_id=match_id,
        duracao_segundos=parse_int(data.get("duracao_segundos"), 0),
        acertos=None,
        require_all_answers=True,
    )
    if error_response:
        return error_response

    return jsonify({"status": "ok", "success": True, "data": result})


@app.get("/api/partidas/<int:match_id>/resultado")
def match_result(match_id):
    token = get_request_token()
    _match, error_response = get_web_match_or_error(match_id, token)
    if error_response:
        return error_response

    result = get_match_result(match_id)
    if not result:
        return json_error("Partida não encontrada.", 404)
    if not result["finalizada"]:
        return json_error("Finalize a partida antes de consultar o resultado.", 400)
    return jsonify({"success": True, "data": result})


@app.get("/api/ranking")
def ranking():
    limit = max(1, min(parse_int(request.args.get("limite"), 10), 100))

    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT usuarios.nome,
                   partidas.acertos,
                   partidas.total_questoes,
                   partidas.duracao_segundos
              FROM partidas
              JOIN usuarios ON usuarios.id = partidas.usuario_id
             WHERE partidas.finalizada = 1
               AND usuarios.consentimento = 1
             ORDER BY partidas.acertos DESC,
                      partidas.duracao_segundos ASC,
                      usuarios.nome ASC
             LIMIT ?
            """,
            (limit,),
        ).fetchall()

    return jsonify(
        [
            {
                "nome": row["nome"],
                "pontos": f"{row['acertos']}/{row['total_questoes']}",
                "tempo": row["duracao_segundos"],
            }
            for row in rows
        ]
    )


@app.post("/api/ednai/analyze")
def ednai_analyze():
    data = get_json_payload()
    if not isinstance(data, dict):
        return json_error("Payload inválido.", 400)

    try:
        return jsonify(ednai_agent.analyze_result(data))
    except GeminiConfigurationError as error:
        logger.warning("Falha de configuração do Ednai: %s", error)
        return jsonify({"erro": str(error)}), 503
    except RuntimeError as error:
        logger.warning("Falha ao consultar Ednai")
        return jsonify({"erro": str(error)}), 503
    except ValueError as error:
        return jsonify({"erro": str(error)}), 400


@app.post("/api/partidas/<int:match_id>/ednai/analyze")
def ednai_analyze_match(match_id):
    data = get_json_payload()
    token = get_request_token(data)
    _match, error_response = get_web_match_or_error(match_id, token)
    if error_response:
        return error_response

    result = get_match_result(match_id, include_items=True)
    if not result:
        return json_error("Partida não encontrada.", 404)
    if not result["finalizada"]:
        return json_error("Finalize a partida antes de solicitar a análise do Ednai.", 400)

    try:
        return jsonify(
            ednai_agent.analyze_result(
                {
                    "session_id": f"partida-{match_id}",
                    "score": result["score"],
                    "total": result["total"],
                    "tempo": result["duracao_segundos"],
                    "mistakes": result["mistakes"],
                    "correct": result["correct"],
                }
            )
        )
    except GeminiConfigurationError as error:
        logger.warning("Falha de configuração do Ednai: %s", error)
        return json_error("A inteligência artificial está indisponível por configuração.", 503)
    except RuntimeError as error:
        logger.warning("Falha ao consultar Ednai: %s", error)
        return json_error("A inteligência artificial está temporariamente indisponível.", 503)
    except ValueError as error:
        return jsonify({"erro": str(error)}), 400


@app.post("/api/partidas/<int:match_id>/ednai/chat")
def ednai_chat_match(match_id):
    data = get_json_payload()
    token = get_request_token(data)
    _match, error_response = get_web_match_or_error(match_id, token)
    if error_response:
        return error_response

    message = str(data.get("message") or data.get("mensagem") or "").strip()
    if not message:
        return json_error("Mensagem obrigatória.", 400)
    if len(message) > 800:
        return json_error("Mensagem muito longa. Envie uma pergunta menor.", 400)

    try:
        return jsonify(
            ednai_agent.chat(
                {
                    "session_id": f"partida-{match_id}",
                    "message": message,
                }
            )
        )
    except GeminiConfigurationError as error:
        logger.warning("Falha de configuração do Ednai: %s", error)
        return json_error("A inteligência artificial está indisponível por configuração.", 503)
    except RuntimeError as error:
        logger.warning("Falha ao consultar Ednai: %s", error)
        return json_error("A inteligência artificial está temporariamente indisponível.", 503)
    except ValueError as error:
        return json_error(str(error), 400)


@app.post("/api/ednai/chat")
def ednai_chat():
    data = get_json_payload()
    if not isinstance(data, dict):
        return json_error("Payload inválido.", 400)

    message = str(data.get("message") or data.get("mensagem") or "").strip()
    if len(message) > 800:
        return json_error("Mensagem muito longa. Envie uma pergunta menor.", 400)

    try:
        return jsonify(ednai_agent.chat(data))
    except GeminiConfigurationError as error:
        logger.warning("Falha de configuração do Ednai: %s", error)
        return jsonify({"erro": str(error)}), 503
    except RuntimeError as error:
        logger.warning("Falha ao consultar Ednai")
        return jsonify({"erro": str(error)}), 503
    except ValueError as error:
        return jsonify({"erro": str(error)}), 400


@app.get("/api/ednai/history")
def ednai_history():
    session_id = str(request.args.get("session_id") or "default").strip() or "default"
    return jsonify(ednai_agent.history(session_id))


if __name__ == "__main__":
    logger.info("Iniciando ednAI em http://0.0.0.0:5000")
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)

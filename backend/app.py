# -*- coding: utf-8 -*-

import random
import sys
from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory

PROJECT_DIR = Path(__file__).resolve().parent.parent
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

try:
    from backend.database import BASE_DIR, get_connection, init_db, row_to_dict
except ModuleNotFoundError:
    from database import BASE_DIR, get_connection, init_db, row_to_dict

from app.ai import EdnaiAgent
from app.ai.gemini_client import GeminiConfigurationError

app = Flask(__name__)
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


def news_payload(row):
    item = row_to_dict(row)
    item["is_fato"] = bool(item["is_fato"])
    item["image_path"] = str((BASE_DIR / item["image_path"]).resolve())
    item["image_url"] = f"{request.host_url.rstrip('/')}/api/imagens/{Path(item['image_path']).name}"
    return item


@app.get("/api/health")
def health():
    return jsonify({"status": "ok"})


@app.get("/api/imagens/<path:filename>")
def serve_image(filename):
    return send_from_directory(BASE_DIR / "news_images", filename)


@app.get("/api/noticias")
def list_news():
    themes_param = request.args.get("temas", "")
    limit = max(1, min(parse_int(request.args.get("limite"), 10), 40))
    themes = [normalize_theme(theme) for theme in themes_param.split(",") if theme.strip()]

    with get_connection() as conn:
        if themes:
            placeholders = ",".join("?" for _ in themes)
            rows = conn.execute(
                f"SELECT * FROM noticias WHERE tema IN ({placeholders})",
                themes,
            ).fetchall()
        else:
            rows = conn.execute("SELECT * FROM noticias").fetchall()

    items = [news_payload(row) for row in rows]
    random.shuffle(items)
    return jsonify(items[:limit])


@app.post("/api/usuarios")
def create_user():
    data = request.get_json(force=True)
    nome = str(data.get("nome", "")).strip()
    idade = parse_int(data.get("idade"), 0)
    consentimento = bool(data.get("consentimento", True))

    if len(nome) < 3 or idade <= 0:
        return jsonify({"erro": "Dados de usuário inválidos"}), 400

    with get_connection() as conn:
        cursor = conn.execute(
            "INSERT INTO usuarios (nome, idade, consentimento) VALUES (?, ?, ?)",
            (nome, idade, int(consentimento)),
        )
        user_id = cursor.lastrowid

    return jsonify({"id": user_id, "nome": nome}), 201


@app.post("/api/partidas")
def create_match():
    data = request.get_json(force=True)
    usuario_id = parse_int(data.get("usuario_id"), 0)
    temas = str(data.get("temas", ""))
    total_questoes = parse_int(data.get("total_questoes"), 0)

    if usuario_id <= 0 or total_questoes <= 0:
        return jsonify({"erro": "Dados de partida inválidos"}), 400

    with get_connection() as conn:
        cursor = conn.execute(
            "INSERT INTO partidas (usuario_id, temas, total_questoes) VALUES (?, ?, ?)",
            (usuario_id, temas, total_questoes),
        )
        match_id = cursor.lastrowid

    return jsonify({"id": match_id}), 201


@app.post("/api/partidas/<int:match_id>/respostas")
def create_answer(match_id):
    data = request.get_json(force=True)
    noticia_id = parse_int(data.get("noticia_id"), 0)
    resposta_jogador = bool(data.get("resposta_jogador", False))
    acertou = bool(data.get("acertou", False))

    if noticia_id <= 0:
        return jsonify({"erro": "Notícia inválida"}), 400

    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO respostas (partida_id, noticia_id, resposta_jogador, acertou)
            VALUES (?, ?, ?, ?)
            """,
            (match_id, noticia_id, int(resposta_jogador), int(acertou)),
        )

    return jsonify({"status": "ok"}), 201


@app.post("/api/partidas/<int:match_id>/finalizar")
def finish_match(match_id):
    data = request.get_json(force=True)
    acertos = parse_int(data.get("acertos"), 0)
    duracao_segundos = parse_int(data.get("duracao_segundos"), 0)

    with get_connection() as conn:
        conn.execute(
            """
            UPDATE partidas
               SET acertos = ?, duracao_segundos = ?, finalizada = 1
             WHERE id = ?
            """,
            (acertos, duracao_segundos, match_id),
        )

    return jsonify({"status": "ok"})


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
    data = request.get_json(force=True)
    if not isinstance(data, dict):
        return jsonify({"erro": "Payload inválido"}), 400

    try:
        return jsonify(ednai_agent.analyze_result(data))
    except GeminiConfigurationError as error:
        return jsonify({"erro": str(error)}), 503
    except RuntimeError as error:
        return jsonify({"erro": str(error)}), 503
    except ValueError as error:
        return jsonify({"erro": str(error)}), 400


@app.post("/api/ednai/chat")
def ednai_chat():
    data = request.get_json(force=True)
    if not isinstance(data, dict):
        return jsonify({"erro": "Payload inválido"}), 400

    try:
        return jsonify(ednai_agent.chat(data))
    except GeminiConfigurationError as error:
        return jsonify({"erro": str(error)}), 503
    except RuntimeError as error:
        return jsonify({"erro": str(error)}), 503
    except ValueError as error:
        return jsonify({"erro": str(error)}), 400


@app.get("/api/ednai/history")
def ednai_history():
    session_id = str(request.args.get("session_id") or "default").strip() or "default"
    return jsonify(ednai_agent.history(session_id))


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True, use_reloader=False)

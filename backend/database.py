# -*- coding: utf-8 -*-

import json
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "ednai.db"
SEED_PATH = BASE_DIR / "news_seed.json"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_connection() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS noticias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tema TEXT NOT NULL,
                manchete TEXT NOT NULL,
                texto TEXT NOT NULL,
                is_fato INTEGER NOT NULL,
                explicacao TEXT NOT NULL,
                fonte TEXT NOT NULL,
                tempo TEXT NOT NULL,
                fonte_url TEXT NOT NULL,
                image_path TEXT NOT NULL UNIQUE
            );

            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                idade INTEGER NOT NULL,
                consentimento INTEGER NOT NULL,
                criado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS partidas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER NOT NULL,
                temas TEXT NOT NULL,
                total_questoes INTEGER NOT NULL,
                acertos INTEGER NOT NULL DEFAULT 0,
                duracao_segundos INTEGER NOT NULL DEFAULT 0,
                finalizada INTEGER NOT NULL DEFAULT 0,
                criada_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
            );

            CREATE TABLE IF NOT EXISTS respostas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                partida_id INTEGER NOT NULL,
                noticia_id INTEGER NOT NULL,
                resposta_jogador INTEGER NOT NULL,
                acertou INTEGER NOT NULL,
                criada_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (partida_id) REFERENCES partidas(id),
                FOREIGN KEY (noticia_id) REFERENCES noticias(id)
            );
            """
        )
    seed_news()


def seed_news():
    if not SEED_PATH.exists():
        return

    with SEED_PATH.open("r", encoding="utf-8") as seed_file:
        news = json.load(seed_file)

    with get_connection() as conn:
        for item in news:
            conn.execute(
                """
                INSERT OR IGNORE INTO noticias (
                    tema, manchete, texto, is_fato, explicacao,
                    fonte, tempo, fonte_url, image_path
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    item["tema"],
                    item["manchete"],
                    item["texto"],
                    int(item["is_fato"]),
                    item["explicacao"],
                    item["fonte"],
                    item["tempo"],
                    item["fonte_url"],
                    item["image_path"],
                ),
            )


def row_to_dict(row):
    return dict(row)


# -*- coding: utf-8 -*-

import json
import re
import shutil
import sys
import zipfile
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
IMAGE_DIR = BASE_DIR / "news_images"
SEED_PATH = BASE_DIR / "news_seed.json"

THEMES = {
    "ciencia": "Ciência",
    "cinema": "Cinema",
    "esportes": "Esportes",
    "tecnologia": "Tecnologia",
}


def slugify(value):
    value = value.lower()
    value = value.replace("ciência", "ciencia")
    value = re.sub(r"[^a-z0-9]+", "_", value)
    return value.strip("_")


def classify(path_parts):
    clean_parts = [slugify(part) for part in path_parts]
    theme_slug = next((part for part in clean_parts if part in THEMES), None)
    if not theme_slug:
        return None

    is_real = "reais" in clean_parts
    is_fake = "fake" in clean_parts or "fakes" in clean_parts
    if not is_real and not is_fake:
        return None

    return THEMES[theme_slug], is_real


def build_news_item(theme, is_real, image_path, index):
    status = "real" if is_real else "fake"
    label = "FATO" if is_real else "FAKE"
    return {
        "tema": theme,
        "manchete": f"Notícia de {theme} - {label} #{index:02d}",
        "texto": "Analise a imagem completa da postagem e decida se a notícia apresentada é fato ou fake.",
        "is_fato": is_real,
        "explicacao": (
            "Esta notícia está marcada como fato no acervo do projeto."
            if is_real
            else "Esta notícia está marcada como fake no acervo do projeto. A explicação detalhada pode ser complementada depois."
        ),
        "fonte": "Acervo ednAI",
        "tempo": "imagem do acervo",
        "fonte_url": "https://www.ufcat.edu.br",
        "image_path": image_path,
        "status": status,
    }


def import_zip(zip_path):
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    counters = {}
    seed_items = []

    with zipfile.ZipFile(zip_path) as archive:
        for info in archive.infolist():
            if info.is_dir():
                continue

            original_path = Path(info.filename)
            if original_path.suffix.lower() not in {".png", ".jpg", ".jpeg"}:
                continue

            classified = classify(original_path.parts)
            if not classified:
                continue

            theme, is_real = classified
            key = (slugify(theme), "real" if is_real else "fake")
            counters[key] = counters.get(key, 0) + 1

            extension = original_path.suffix.lower().replace(".jpg", ".jpeg")
            filename = f"{key[0]}_{key[1]}_{counters[key]:02d}{extension}"
            target_path = IMAGE_DIR / filename

            with archive.open(info) as source, target_path.open("wb") as target:
                shutil.copyfileobj(source, target)

            seed_items.append(
                build_news_item(
                    theme=theme,
                    is_real=is_real,
                    image_path=f"news_images/{filename}",
                    index=counters[key],
                )
            )

    with SEED_PATH.open("w", encoding="utf-8") as seed_file:
        json.dump(seed_items, seed_file, ensure_ascii=False, indent=2)

    return len(seed_items)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python3 backend/seed_news_from_zip.py /caminho/para/noticias.zip")
        raise SystemExit(1)

    total = import_zip(Path(sys.argv[1]))
    print(f"{total} notícias importadas para {SEED_PATH}")


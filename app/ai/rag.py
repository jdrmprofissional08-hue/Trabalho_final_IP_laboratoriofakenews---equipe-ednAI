# -*- coding: utf-8 -*-

from __future__ import annotations

import hashlib
import math
import re
from threading import RLock
from pathlib import Path


AI_DIR = Path(__file__).resolve().parent
KNOWLEDGE_DIR = AI_DIR / "knowledge"
CHROMA_DIR = AI_DIR / ".chroma"


class HashEmbeddingFunction:
    def __init__(self, dimensions: int = 384):
        self.dimensions = dimensions

    def name(self) -> str:
        return "ednai_hash_embedding"

    def __call__(self, input: list[str]) -> list[list[float]]:
        return [self._embed(text) for text in input]

    def embed_query(self, input: str | list[str]) -> list[float] | list[list[float]]:
        if isinstance(input, str):
            return self._embed(input)
        return self(input)

    def embed_documents(self, input: list[str]) -> list[list[float]]:
        return self(input)

    def _embed(self, text: str) -> list[float]:
        vector = [0.0] * self.dimensions
        tokens = re.findall(r"[\wÀ-ÿ]{2,}", text.lower())
        for token in tokens:
            digest = hashlib.sha256(token.encode("utf-8")).digest()
            index = int.from_bytes(digest[:4], "big") % self.dimensions
            sign = 1.0 if digest[4] % 2 == 0 else -1.0
            vector[index] += sign
        norm = math.sqrt(sum(value * value for value in vector))
        if norm:
            vector = [value / norm for value in vector]
        return vector


class RagKnowledgeBase:
    def __init__(
        self,
        knowledge_dir: Path = KNOWLEDGE_DIR,
        chroma_dir: Path = CHROMA_DIR,
        collection_name: str = "ednai_knowledge",
    ):
        self.knowledge_dir = knowledge_dir
        self.chroma_dir = chroma_dir
        self.collection_name = collection_name
        self.embedding_function = HashEmbeddingFunction()
        self._collection = None
        self._indexed_signature = ""
        self._lock = RLock()

    def search(self, query: str, limit: int = 5) -> str:
        self.index_documents()
        collection = self._get_collection()
        if collection.count() == 0:
            return ""

        n_results = min(max(limit, 1), collection.count())
        result = collection.query(query_texts=[query], n_results=n_results)
        documents = result.get("documents", [[]])[0]
        metadatas = result.get("metadatas", [[]])[0]

        parts: list[str] = []
        for document, metadata in zip(documents, metadatas):
            source = metadata.get("source", "fonte desconhecida") if isinstance(metadata, dict) else "fonte desconhecida"
            parts.append(f"Fonte: {source}\n{document}")
        return "\n\n---\n\n".join(parts)

    def index_documents(self) -> int:
        with self._lock:
            collection = self._get_collection()
            self.knowledge_dir.mkdir(parents=True, exist_ok=True)
            paths = sorted(self.knowledge_dir.glob("*.md"))
            signature = self._signature(paths)
            if signature == self._indexed_signature:
                return collection.count()

            ids: list[str] = []
            documents: list[str] = []
            metadatas: list[dict[str, str]] = []

            for path in paths:
                content = path.read_text(encoding="utf-8").strip()
                for index, chunk in enumerate(self._split(content), start=1):
                    ids.append(f"{path.stem}-{index}")
                    documents.append(chunk)
                    metadatas.append({"source": path.name})

            existing = collection.get(include=[])
            existing_ids = existing.get("ids", [])
            if existing_ids:
                collection.delete(ids=existing_ids)
            if documents:
                collection.upsert(ids=ids, documents=documents, metadatas=metadatas)

            self._indexed_signature = signature
            return len(documents)

    def _get_collection(self):
        if self._collection is not None:
            return self._collection

        try:
            import chromadb
        except ImportError as error:
            raise RuntimeError("ChromaDB não está instalado. Execute: pip install chromadb") from error

        self.chroma_dir.mkdir(parents=True, exist_ok=True)
        client = chromadb.PersistentClient(path=str(self.chroma_dir))
        self._collection = client.get_or_create_collection(
            name=self.collection_name,
            embedding_function=self.embedding_function,
        )
        return self._collection

    def _split(self, content: str, max_chars: int = 1200) -> list[str]:
        blocks = [block.strip() for block in re.split(r"\n\s*\n", content) if block.strip()]
        chunks: list[str] = []
        current = ""
        for block in blocks:
            if len(current) + len(block) + 2 <= max_chars:
                current = f"{current}\n\n{block}".strip()
                continue
            if current:
                chunks.append(current)
            current = block
        if current:
            chunks.append(current)
        return chunks

    def _signature(self, paths: list[Path]) -> str:
        digest = hashlib.sha256()
        for path in paths:
            stat = path.stat()
            digest.update(str(path.name).encode("utf-8"))
            digest.update(str(stat.st_mtime_ns).encode("utf-8"))
            digest.update(str(stat.st_size).encode("utf-8"))
        return digest.hexdigest()

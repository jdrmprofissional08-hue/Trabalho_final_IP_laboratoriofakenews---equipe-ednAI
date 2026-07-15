# -*- coding: utf-8 -*-

from __future__ import annotations

from typing import Any

from .gemini_client import GeminiClient
from .memory import ConversationMemory
from .prompts import SYSTEM_PROMPT, build_analysis_prompt, build_chat_prompt
from .rag import RagKnowledgeBase


class EdnaiAgent:
    def __init__(
        self,
        gemini: GeminiClient | None = None,
        memory: ConversationMemory | None = None,
        rag: RagKnowledgeBase | None = None,
    ):
        self.gemini = gemini or GeminiClient()
        self.memory = memory or ConversationMemory()
        self.rag = rag or RagKnowledgeBase()

    def analyze_result(self, payload: dict[str, Any]) -> dict[str, Any]:
        session_id = self._session_id(payload)
        game_result = self._sanitize_game_result(payload)
        self.memory.set_game_context(session_id, game_result)

        query = self._query_from_result(game_result)
        rag_context = self.rag.search(query)
        prompt = build_analysis_prompt(game_result=game_result, rag_context=rag_context)
        answer = self.gemini.generate(SYSTEM_PROMPT, prompt)

        self.memory.add_message(session_id, "user", "Análise inicial do resultado do desafio.")
        self.memory.add_message(session_id, "assistant", answer)

        return {
            "session_id": session_id,
            "resposta": answer,
        }

    def chat(self, payload: dict[str, Any]) -> dict[str, Any]:
        session_id = self._session_id(payload)
        question = str(payload.get("message") or payload.get("mensagem") or "").strip()
        if not question:
            raise ValueError("Mensagem obrigatória.")

        history = self.memory.history(session_id)
        game_context = self.memory.get_game_context(session_id)
        rag_context = self.rag.search(question)
        prompt = build_chat_prompt(
            question=question,
            game_context=game_context,
            conversation_history=history,
            rag_context=rag_context,
        )
        answer = self.gemini.generate(SYSTEM_PROMPT, prompt)

        self.memory.add_message(session_id, "user", question)
        self.memory.add_message(session_id, "assistant", answer)

        return {
            "session_id": session_id,
            "resposta": answer,
        }

    def history(self, session_id: str) -> dict[str, Any]:
        return self.memory.export(session_id)

    def _sanitize_game_result(self, payload: dict[str, Any]) -> dict[str, Any]:
        result = payload.get("result") if isinstance(payload.get("result"), dict) else payload
        return {
            "score": result.get("score", result.get("acertos")),
            "total": result.get("total"),
            "tempo": result.get("tempo", result.get("duracao_segundos")),
            "mistakes": self._sanitize_items(result.get("mistakes", result.get("erros", []))),
            "correct": self._sanitize_items(result.get("correct", result.get("acertos_lista", []))),
        }

    def _sanitize_items(self, items: Any, limit: int = 10) -> list[dict[str, Any]]:
        if not isinstance(items, list):
            return []

        sanitized = []
        for item in items[:limit]:
            if not isinstance(item, dict):
                continue
            sanitized.append(
                {
                    "id": item.get("id"),
                    "tema": item.get("tema"),
                    "manchete": self._truncate(item.get("manchete")),
                    "texto": self._truncate(item.get("texto"), 600),
                    "resposta_jogador": item.get("resposta_jogador"),
                    "is_fato": item.get("is_fato"),
                    "explicacao": self._truncate(item.get("explicacao"), 700),
                }
            )
        return sanitized

    def _query_from_result(self, game_result: dict[str, Any]) -> str:
        headlines = [
            str(item.get("manchete", ""))
            for key in ("mistakes", "correct")
            for item in game_result.get(key, [])
        ]
        return "fake news educação midiática checagem de fatos " + " ".join(headlines[:10])

    def _session_id(self, payload: dict[str, Any]) -> str:
        return str(payload.get("session_id") or payload.get("partida_id") or "default").strip() or "default"

    def _truncate(self, value: Any, max_chars: int = 500) -> str:
        text = str(value or "").strip()
        if len(text) <= max_chars:
            return text
        return text[:max_chars].rstrip() + "..."

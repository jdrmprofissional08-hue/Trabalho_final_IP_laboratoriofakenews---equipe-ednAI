# -*- coding: utf-8 -*-

from __future__ import annotations

from collections import defaultdict
from copy import deepcopy
from dataclasses import dataclass, field
from threading import RLock
from time import time
from typing import Any


@dataclass
class ConversationState:
    messages: list[dict[str, str]] = field(default_factory=list)
    game_context: dict[str, Any] | None = None
    updated_at: float = field(default_factory=time)


class ConversationMemory:
    def __init__(self, max_messages: int = 12):
        self.max_messages = max_messages
        self._lock = RLock()
        self._sessions: dict[str, ConversationState] = defaultdict(ConversationState)

    def set_game_context(self, session_id: str, context: dict[str, Any]) -> None:
        with self._lock:
            state = self._sessions[session_id]
            state.game_context = deepcopy(context)
            state.updated_at = time()

    def get_game_context(self, session_id: str) -> dict[str, Any] | None:
        with self._lock:
            context = self._sessions[session_id].game_context
            return deepcopy(context) if context is not None else None

    def add_message(self, session_id: str, role: str, content: str) -> None:
        with self._lock:
            state = self._sessions[session_id]
            state.messages.append({"role": role, "content": content})
            state.messages = state.messages[-self.max_messages :]
            state.updated_at = time()

    def history(self, session_id: str) -> list[dict[str, str]]:
        with self._lock:
            return deepcopy(self._sessions[session_id].messages)

    def export(self, session_id: str) -> dict[str, Any]:
        with self._lock:
            state = self._sessions[session_id]
            return {
                "session_id": session_id,
                "messages": deepcopy(state.messages),
                "game_context": deepcopy(state.game_context),
                "updated_at": state.updated_at,
            }

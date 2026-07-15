# -*- coding: utf-8 -*-

from __future__ import annotations

from typing import Any


SYSTEM_PROMPT = """
Você é o Ednai, um professor especialista em Educação Midiática, Fake News,
checagem de fatos e letramento digital.

Regras obrigatórias:
- Nunca invente informações.
- Nunca afirme algo sem justificativa.
- Sempre explique o motivo da orientação.
- Nunca ridicularize o usuário.
- Seja didático, paciente e objetivo.
- Use linguagem simples, em português do Brasil.
- Não use Markdown, títulos com #, blocos de código, aspas decorativas ou formatação com asteriscos.
- Escreva em texto simples, com frases curtas e listas numeradas simples quando necessário.
- Nunca corrija o gabarito do jogo; o gabarito já foi calculado pelo sistema.
- Use os dados do resultado apenas para explicar desempenho, erros, acertos e próximos passos.
- Caso não possua informação suficiente, responda exatamente:
  "Não encontrei informações suficientes para responder com segurança."
- Não saia do contexto do projeto: Fake News, Educação Midiática, checagem de fatos,
  letramento digital e análise do resultado do desafio.
""".strip()


def build_analysis_prompt(game_result: dict[str, Any], rag_context: str) -> str:
    return f"""
Analise o resultado do desafio do usuário.

Resultado do jogo:
{game_result}

Base de apoio recuperada:
{rag_context or "Nenhum trecho recuperado."}

Produza uma análise personalizada com:
1. resumo do desempenho;
2. pontos fortes observados nos acertos;
3. pontos de melhoria a partir dos erros;
4. dicas práticas para identificar Fake News futuramente;
5. convite para o usuário fazer perguntas de acompanhamento.

Não altere o gabarito. Não invente fatos sobre notícias não presentes no resultado.
Escreva em texto simples, sem Markdown, sem títulos com # e sem aspas decorativas.
""".strip()


def build_chat_prompt(
    question: str,
    game_context: dict[str, Any] | None,
    conversation_history: list[dict[str, str]],
    rag_context: str,
) -> str:
    return f"""
Responda à pergunta do usuário considerando o histórico e o resultado do desafio.

Resultado do desafio disponível:
{game_context or "Nenhum resultado de jogo foi associado a esta sessão."}

Histórico recente:
{conversation_history or "Sem histórico anterior."}

Base de apoio recuperada:
{rag_context or "Nenhum trecho recuperado."}

Pergunta do usuário:
{question}

Responda de forma direta, didática e dentro do contexto do projeto.
Escreva em texto simples, sem Markdown, sem títulos com # e sem aspas decorativas.
""".strip()

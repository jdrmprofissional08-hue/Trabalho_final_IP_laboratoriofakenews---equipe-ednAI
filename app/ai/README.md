# Ednai

Módulo do agente de IA do projeto.

## Componentes

- `agent.py`: orquestra análise, chat, memória, RAG e Gemini.
- `gemini_client.py`: encapsula a API oficial `google-genai`.
- `prompts.py`: contém prompt de sistema e builders de prompt.
- `memory.py`: mantém histórico simples por sessão em memória.
- `rag.py`: indexa e consulta documentos Markdown com ChromaDB.
- `knowledge/`: base inicial de conhecimento editável.

## Variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
GEMINI_API_KEY=sua_chave_aqui
GEMINI_API_KEY_2=sua_segunda_chave_opcional
GEMINI_API_KEY_3=sua_terceira_chave_opcional
GEMINI_MODEL=gemini-3.1-flash-lite
```

Nunca coloque a chave no código.

O cliente tenta as chaves em ordem. Se uma chave bater cota, limite de taxa,
indisponibilidade temporária ou erro de permissão, ele tenta a próxima.

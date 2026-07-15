# ednAI — Laboratório de Combate a Fake News

Aplicação educacional para treinar verificação de informações. O projeto combina:

- interface desktop em `PySide6`;
- backend local em `Flask`;
- persistência em `SQLite`;
- acervo local de notícias;
- ranking de partidas;
- agente educacional `Ednai`, integrado ao Gemini e apoiado por uma base RAG local com ChromaDB.

O jogo corrige as respostas automaticamente. O agente não decide se uma notícia é `FATO` ou `FAKE`; ele entra depois da correção para explicar desempenho, erros, acertos e boas práticas de educação midiática.

## Fluxo Do Produto

```text
Usuário informa nome, idade e temas
↓
Backend carrega notícias do acervo
↓
Usuário responde FATO ou FAKE
↓
Sistema corrige pelo gabarito cadastrado
↓
Feedback educativo é exibido após cada resposta
↓
Resultado e ranking são atualizados
↓
Ednai analisa desempenho e abre chat de acompanhamento
```

## Arquitetura

```text
PySide6
  └── main.py
      └── Backend Flask
          ├── SQLite
          ├── Acervo de notícias
          └── Ednai
              ├── Prompt de sistema
              ├── Memória em sessão
              ├── RAG local com ChromaDB
              ├── Gemini API
              └── Resposta educativa
```

O backend atual é `Flask`. A arquitetura do agente foi adicionada seguindo esse padrão para evitar uma migração desnecessária para outro framework.

## Estrutura De Pastas

```text
.
├── app/
│   └── ai/
│       ├── agent.py
│       ├── gemini_client.py
│       ├── memory.py
│       ├── prompts.py
│       ├── rag.py
│       ├── knowledge/
│       └── README.md
├── backend/
│   ├── app.py
│   ├── database.py
│   ├── news_seed.json
│   └── news_images/
├── src/
│   └── ui/
├── main.py
├── requirements.txt
└── .env.example
```

## Componentes Principais

### Interface

- `main.py`: coordena telas, estado da partida, comunicação HTTP com o backend e chamadas ao Ednai.
- `src/ui/tela_inicial.py`: formulário inicial.
- `src/ui/tela_quiz.py`: exibição das notícias e respostas `FATO`/`FAKE`.
- `src/ui/tela_feedback.py`: feedback após cada resposta.
- `src/ui/tela_final.py`: resultado final, análise do Ednai e chat.
- `src/ui/tela_ranking.py`: ranking.

### Backend

- `backend/app.py`: rotas HTTP do jogo e do Ednai.
- `backend/database.py`: criação e acesso ao SQLite.
- `backend/news_seed.json`: gabarito e metadados das notícias.
- `backend/news_images/`: imagens exibidas no quiz.

### Ednai

- `app/ai/agent.py`: orquestra análise, chat, memória, RAG e Gemini.
- `app/ai/gemini_client.py`: encapsula `google-genai`, lê `.env` e faz fallback entre múltiplas chaves.
- `app/ai/memory.py`: histórico simples por sessão em memória.
- `app/ai/prompts.py`: prompt de sistema e prompts de análise/chat.
- `app/ai/rag.py`: indexação e consulta ChromaDB com embeddings determinísticos leves.
- `app/ai/knowledge/`: documentos Markdown usados como base de apoio.

## Variáveis De Ambiente

Crie um arquivo `.env` na raiz do projeto. Use `.env.example` como base:

```env
GEMINI_API_KEY=sua_chave_principal
GEMINI_API_KEY_2=sua_segunda_chave_opcional
GEMINI_API_KEY_3=sua_terceira_chave_opcional

GEMINI_MODEL=gemini-3.1-flash-lite
GEMINI_TEMPERATURE=0.3
```

Também é aceito:

```env
GEMINI_API_KEYS=chave_1,chave_2,chave_3
```

Regras:

- Nunca coloque chaves no código.
- `.env` está no `.gitignore`.
- O cliente tenta as chaves em ordem.
- Se uma chave bater cota, limite de taxa, indisponibilidade temporária ou erro de permissão, a próxima é usada automaticamente.

## Instalação

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Execução

Terminal 1 — backend:

```bash
venv/bin/python backend/app.py
```

Terminal 2 — interface:

```bash
venv/bin/python main.py
```

Teste rápido do backend:

```bash
curl http://127.0.0.1:5000/api/health
```

Resposta esperada:

```json
{"status":"ok"}
```

## Endpoints Do Jogo

### `GET /api/health`

Verifica se o backend está ativo.

### `GET /api/imagens/<filename>`

Serve imagens do acervo.

### `GET /api/noticias?temas=Ciência,Tecnologia&limite=10`

Retorna notícias do acervo, embaralhadas e filtradas por tema.

### `POST /api/usuarios`

Cria um usuário da partida.

```json
{
  "nome": "Maria",
  "idade": 21,
  "consentimento": true
}
```

### `POST /api/partidas`

Cria uma partida.

```json
{
  "usuario_id": 1,
  "temas": "Ciência,Tecnologia",
  "total_questoes": 10
}
```

### `POST /api/partidas/<id>/respostas`

Registra uma resposta.

```json
{
  "noticia_id": 3,
  "resposta_jogador": true,
  "acertou": false
}
```

### `POST /api/partidas/<id>/finalizar`

Finaliza a partida.

```json
{
  "acertos": 8,
  "duracao_segundos": 120
}
```

### `GET /api/ranking?limite=10`

Retorna o ranking.

## Endpoints Do Ednai

### `POST /api/ednai/analyze`

Recebe o resultado corrigido pelo sistema e gera uma análise personalizada.

```json
{
  "session_id": "partida-123",
  "score": 8,
  "total": 10,
  "tempo": 120,
  "mistakes": [],
  "correct": []
}
```

Resposta:

```json
{
  "session_id": "partida-123",
  "resposta": "..."
}
```

### `POST /api/ednai/chat`

Continua a conversa usando o histórico da sessão.

```json
{
  "session_id": "partida-123",
  "message": "Por que errei a notícia 4?"
}
```

### `GET /api/ednai/history?session_id=partida-123`

Retorna o histórico em memória da sessão.

## RAG

A base RAG fica em:

```text
app/ai/knowledge/
```

Para adicionar conhecimento novo:

1. crie ou edite um arquivo `.md` nessa pasta;
2. reinicie o backend ou faça uma nova consulta;
3. o índice local será atualizado automaticamente se detectar mudança nos arquivos.

O índice ChromaDB é gerado em runtime em `app/ai/.chroma/` e não deve ser versionado.

## Segurança E Privacidade

- O Ednai recebe apenas dados sanitizados da partida.
- Textos longos são truncados antes de serem enviados ao Gemini.
- A correção do quiz não depende do Gemini.
- O gabarito cadastrado continua sendo a fonte de verdade.
- Chaves de API ficam exclusivamente no `.env`.
- O histórico de conversa atual é em memória; ao reiniciar o backend, ele é perdido.

## Limitações Atuais

- A interface é desktop `PySide6`.
- O backend roda localmente em `127.0.0.1:5000` por padrão.
- A memória do Ednai não é persistida em banco.
- O RAG usa embeddings determinísticos leves para manter baixo consumo local.
- A qualidade da resposta depende do modelo Gemini configurado e da cota disponível.

## Solução De Problemas

### Porta 5000 ocupada

```bash
lsof -i :5000
pkill -f "backend/app.py"
venv/bin/python backend/app.py
```

### Ednai não responde

Verifique:

1. backend está rodando;
2. `.env` tem pelo menos uma chave Gemini preenchida;
3. `GEMINI_MODEL` está em um modelo disponível para sua conta;
4. dependências foram instaladas com `pip install -r requirements.txt`;
5. há cota disponível nas chaves configuradas.

### Testar RAG local

```bash
venv/bin/python - <<'PY'
from app.ai.rag import RagKnowledgeBase
rag = RagKnowledgeBase()
print(rag.index_documents())
print(rag.search("como identificar fake news", limit=2))
PY
```

### Testar histórico do Ednai

```bash
curl "http://127.0.0.1:5000/api/ednai/history?session_id=teste"
```

## Implementação Ativa

A implementação ativa do agente está concentrada em `app/ai/` e é chamada somente após a correção automática do quiz. O restante do sistema permanece responsável pelo jogo, persistência, ranking e exibição das notícias.

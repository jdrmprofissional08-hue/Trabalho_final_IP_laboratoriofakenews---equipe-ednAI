# ednAI — Laboratório de Combate a Fake News

Aplicação educacional para treinar verificação de informações, com duas interfaces mantidas no mesmo repositório:

1. Interface desktop desenvolvida com `PySide6`.
2. Interface web desenvolvida com `HTML`, `CSS` e `JavaScript`.

Ambas utilizam o mesmo backend `Flask`, o mesmo banco `SQLite`, as mesmas notícias, as mesmas regras do quiz, o mesmo ranking e a mesma integração com o agente educacional `Ednai`/Gemini.

O jogo corrige as respostas automaticamente. O agente não decide se uma notícia é `FATO` ou `FAKE`; ele entra depois da correção para explicar desempenho, erros, acertos e boas práticas de educação midiática.

## Visão Geral

O ednAI combina:

- interface desktop em `PySide6`;
- interface web responsiva para navegador e celular;
- backend local em `Flask`;
- persistência em `SQLite`;
- acervo local de notícias;
- ranking de partidas;
- agente educacional `Ednai`, integrado ao Gemini e apoiado por uma base RAG local com ChromaDB.

## Arquitetura

```text
Desktop PySide6 ─┐
                 ├── Backend Flask ── SQLite
Web HTML/CSS/JS ─┘                  └─ Ednai/Gemini
```

A interface desktop e a interface web são independentes na camada visual, mas compartilham a mesma API Flask. Não existem dois backends nem dois bancos de dados.

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

## Versão Desktop

A versão desktop original continua sendo executada por:

```bash
python main.py
```

Ela usa `PySide6` e se comunica com o backend Flask em:

```text
http://127.0.0.1:5000
```

## Versão Web

A versão web é servida pelo próprio Flask em:

```text
http://localhost:5000
```

Ela usa URLs relativas, como `/api/...`, para funcionar tanto localmente quanto por Cloudflare Tunnel.

## Instalação

Crie o ambiente virtual:

```bash
python -m venv venv
```

Ative no Windows:

```bash
venv\Scripts\activate
```

Ative no Linux/macOS:

```bash
source venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

## Configuração Do `.env`

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

- nunca coloque chaves no código;
- nunca coloque chaves no HTML, CSS ou JavaScript;
- `.env` está no `.gitignore`;
- o cliente tenta as chaves em ordem;
- se uma chave bater cota, limite de taxa, indisponibilidade temporária ou erro de permissão, a próxima é usada automaticamente.

## Como Executar O Backend

```bash
python backend/app.py
```

O servidor Flask sobe em:

```text
http://localhost:5000
```

Teste rápido:

```bash
curl http://127.0.0.1:5000/api/health
```

Resposta esperada:

```json
{"status":"ok"}
```

## Como Executar O Desktop

Com o backend aberto em outro terminal:

```bash
python main.py
```

## Como Acessar A Interface Web

Com o backend aberto, acesse no navegador:

```text
http://localhost:5000
```

Páginas principais:

- `/`: tela inicial;
- `/quiz`: tela do quiz;
- `/resultado`: resultado final;
- `/ranking`: ranking geral.

## Cloudflare Tunnel

Antes de abrir o túnel, instale o `cloudflared`.

### Windows

Opção simples com Winget:

```bash
winget install --id Cloudflare.cloudflared
```

Se o Winget não estiver disponível, baixe o instalador em:

```text
https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/
```

### Linux

Em distribuições Debian/Ubuntu, baixe o pacote `.deb` mais recente na página oficial da Cloudflare:

```text
https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/
```

Depois instale o arquivo baixado:

```bash
sudo dpkg -i cloudflared-linux-amd64.deb
```

### macOS

Com Homebrew:

```bash
brew install cloudflared
```

Confirme a instalação:

```bash
cloudflared --version
```

Com o Flask rodando, execute:

```bash
cloudflared tunnel --url http://localhost:5000
```

O Cloudflare exibirá um link público temporário. Esse link poderá ser aberto em outro computador ou celular, inclusive fora da mesma rede Wi-Fi.

O computador que hospeda o projeto precisa permanecer:

- ligado;
- conectado à internet;
- com o Flask aberto;
- com o Cloudflare Tunnel aberto.

O link do Quick Tunnel pode mudar sempre que o comando for reiniciado.

## Como Gerar QR Code

Use o link público gerado pelo Cloudflare Tunnel em qualquer gerador de QR Code confiável.

Fluxo sugerido para apresentação:

1. iniciar `python backend/app.py`;
2. iniciar `cloudflared tunnel --url http://localhost:5000`;
3. copiar o link público gerado;
4. gerar o QR Code com esse link;
5. testar o QR Code em um celular usando 4G/5G.

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
├── web/
│   ├── templates/
│   │   ├── index.html
│   │   ├── quiz.html
│   │   ├── resultado.html
│   │   ├── ranking.html
│   │   └── erro.html
│   └── static/
│       ├── css/
│       │   └── style.css
│       ├── images/
│       └── js/
│           ├── common.js
│           ├── inicio.js
│           ├── quiz.js
│           ├── resultado.js
│           └── ranking.js
├── main.py
├── requirements.txt
└── .env.example
```

## Componentes Principais

### Interface Desktop

- `main.py`: coordena telas, estado da partida, comunicação HTTP com o backend e chamadas ao Ednai.
- `src/ui/tela_inicial.py`: formulário inicial.
- `src/ui/tela_quiz.py`: exibição das notícias e respostas `FATO`/`FAKE`.
- `src/ui/tela_feedback.py`: feedback após cada resposta.
- `src/ui/tela_final.py`: resultado final, análise do Ednai e chat.
- `src/ui/tela_ranking.py`: ranking.

### Interface Web

- `web/templates/`: páginas HTML servidas pelo Flask.
- `web/static/css/style.css`: identidade visual e responsividade.
- `web/static/js/common.js`: utilitários de API, estado mínimo da partida e mensagens.
- `web/static/js/inicio.js`: criação da partida web.
- `web/static/js/quiz.js`: fluxo do quiz web.
- `web/static/js/resultado.js`: resultado e conversa com Ednai.
- `web/static/js/ranking.js`: carregamento do ranking.

### Backend

- `backend/app.py`: rotas HTTP do jogo, da interface web e do Ednai.
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

## Endpoints Principais

### Páginas Web

- `GET /`
- `GET /quiz`
- `GET /resultado`
- `GET /ranking`

### API Do Jogo

- `GET /api/health`
- `GET /api/imagens/<filename>`
- `GET /api/temas`
- `GET /api/noticias?temas=Ciência,Tecnologia&limite=10`
- `GET /api/noticias-web?temas=Ciência,Tecnologia&limite=10`
- `POST /api/usuarios`
- `POST /api/partidas`
- `POST /api/web/partidas` — cria usuário, partida, token web e seleção de notícias.
- `GET /api/partidas/<id>/questao` — requer token web em `X-Partida-Token`.
- `POST /api/partidas/<id>/respostas`
- `POST /api/partidas/<id>/responder` — requer token web e corrige no backend.
- `POST /api/partidas/<id>/finalizar`
- `POST /api/web/partidas/<id>/finalizar` — requer token web e ignora pontuação enviada pelo navegador.
- `GET /api/partidas/<id>/resultado` — requer token web.
- `GET /api/ranking?limite=10`

### API Do Ednai

- `POST /api/ednai/analyze`
- `POST /api/partidas/<id>/ednai/analyze` — requer token web e busca resultado no banco.
- `POST /api/partidas/<id>/ednai/chat` — requer token web.
- `POST /api/ednai/chat`
- `GET /api/ednai/history?session_id=partida-1`

## Cuidados De Segurança

- O Flask é executado com `debug=False`.
- A chave Gemini fica somente no backend.
- O JavaScript chama apenas rotas relativas.
- A rota web de notícias não envia `is_fato` nem o gabarito completo.
- A correção da versão web é feita pelo backend em `/api/partidas/<id>/responder`.
- O resultado da versão web é calculado pelo backend ao finalizar a partida.
- As rotas web sensíveis usam um token aleatório por partida, além do ID numérico.
- O navegador armazena apenas `usuarioId`, `partidaId`, `token`, índice atual, total e tempo inicial em `sessionStorage`.
- A rota de imagens usa diretório fixo e rejeita caminho com subpastas.
- Não habilite CORS aberto, pois frontend e backend são servidos pelo mesmo Flask.

## Limitações Conhecidas

- O banco `SQLite` é adequado para apresentação local e túnel temporário, mas não é ideal para muitos usuários simultâneos em produção.
- O token web protege contra troca casual de IDs, mas não substitui autenticação real de usuários.
- O Cloudflare Quick Tunnel gera link temporário e pode mudar ao reiniciar o comando.
- A análise do Ednai depende de chave Gemini válida, internet e disponibilidade da API.
- A interface desktop ainda possui fallback local para notícias caso o backend esteja indisponível.

## Testes Recomendados

### Backend

```bash
python backend/app.py
curl http://127.0.0.1:5000/api/health
```

### Web

Abra:

```text
http://localhost:5000
```

Valide:

- tela inicial;
- CSS e JavaScript;
- início de partida;
- carregamento de notícias;
- imagens;
- envio de respostas;
- feedback;
- resultado;
- ranking;
- Ednai, quando a chave estiver configurada.

### Desktop

Com o backend aberto:

```bash
python main.py
```

Valide:

- abertura da interface;
- criação de usuário;
- início da partida;
- envio de respostas;
- finalização;
- ranking;
- comunicação com a IA.

### Responsividade

Teste no modo responsivo do navegador:

- `320px`;
- `375px`;
- `390px`;
- `768px`.

### Túnel

```bash
cloudflared tunnel --url http://localhost:5000
```

Teste o link gerado:

- no próprio computador;
- em celular na mesma rede;
- em celular usando 4G/5G.

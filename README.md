# ednAI - Laboratório de Combate a Fake News

Aplicação em Python para a disciplina de Introdução à Programação (UFCAT), com interface gráfica em `PySide6`, backend local em `Flask` e banco `SQLite`.

## Apresentação

O projeto é um jogo educativo de verificação de notícias. O usuário informa seus dados, escolhe um tema de interesse e responde se cada postagem é fato ou fake.

As notícias são carregadas pelo backend a partir de um acervo com imagens completas, separadas por tema e classificação. Ao final da partida, o sistema registra a pontuação e exibe o ranking geral.

## Objetivos do Projeto

- Desenvolver uma aplicação interativa em Python.
- Aplicar conceitos de controle de fluxo, funções, listas e organização modular.
- Explorar interface gráfica com `PySide6`.
- Armazenar participantes, partidas, respostas e ranking em banco local.
- Exibir a imagem completa da postagem durante o quiz.
- Exibir feedback educativo após cada resposta.

## Fluxo da Aplicação

1. Tela inicial com nome, idade, consentimento e tema de interesse.
2. Tela de quiz com imagem da postagem, manchete, contexto e botões `É FATO` e `É FAKE`.
3. Tela de feedback com explicação da resposta.
4. Tela final com pontuação.
5. Tela de ranking com histórico das partidas autorizadas.

## Temas Disponíveis

- Ciência
- Cinema
- Esportes
- Tecnologia

## Estrutura do Projeto

```text
trabalho_final_ip_laboratoriofakenews---equipe-ednAI/
├── main.py
├── requirements.txt
├── backend/
│   ├── __init__.py
│   ├── app.py
│   ├── database.py
│   ├── seed_news_from_zip.py
│   ├── news_seed.json
│   └── news_images/
└── src/
    ├── styles.py
    └── ui/
        ├── components.py
        ├── tela_inicial.py
        ├── tela_quiz.py
        ├── tela_feedback.py
        ├── tela_final.py
        └── tela_ranking.py
```

## Tecnologias Utilizadas

- Python 3.10+
- PySide6
- Flask
- requests
- SQLite

## Requisitos da Disciplina

O projeto foi organizado para atender os requisitos principais da especificação:

- arquivo principal de execução em `main.py`;
- separação por módulos;
- interface gráfica;
- uso de biblioteca Python externa;
- persistência local com banco de dados;
- documentação básica do projeto.

## Como Executar

1. Crie e ative um ambiente virtual:

```bash
python3 -m venv venv
source venv/bin/activate
```

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Inicie o backend em um terminal:

```bash
python3 backend/app.py
```

4. Em outro terminal, ative o ambiente virtual novamente:

```bash
source venv/bin/activate
```

5. Inicie a interface gráfica:

```bash
python3 main.py
```

Durante o quiz, a tela mostra a imagem da postagem, um cronômetro e um contador de progresso.

## Backend

O backend local fornece:

- notícias filtradas por tema;
- imagens completas das postagens;
- cadastro dos participantes;
- registro das partidas e respostas;
- ranking geral com pontuação e tempo.

Rotas principais:

- `GET /api/health`
- `GET /api/noticias`
- `GET /api/imagens/<arquivo>`
- `POST /api/usuarios`
- `POST /api/partidas`
- `POST /api/partidas/<id>/respostas`
- `POST /api/partidas/<id>/finalizar`
- `GET /api/ranking`

## Banco de Dados

O banco `SQLite` é criado automaticamente em `backend/ednai.db` quando o backend é iniciado.

Tabelas principais:

- `noticias`: armazena tema, texto, classificação e caminho da imagem.
- `usuarios`: armazena nome, idade e consentimento do participante.
- `partidas`: armazena tema, pontuação, duração e status da partida.
- `respostas`: armazena cada resposta dada durante o quiz.

O arquivo `backend/ednai.db` é gerado localmente e não precisa ser versionado no Git.

## Importação de Notícias

O acervo atual já está importado em `backend/news_seed.json` e `backend/news_images/`.

Para importar novamente a partir de um arquivo `.zip` com a mesma organização de pastas:

```bash
python3 backend/seed_news_from_zip.py /caminho/para/noticias.zip
```

Depois disso, reinicie o backend para recriar ou atualizar as notícias no banco.

# ednAI - Laboratório de Combate a Fake News

Aplicação em Python para a disciplina de Introdução à Programação (UFCAT), com interface gráfica em `PySide6`, backend local em `Flask` e banco `SQLite`.

## Apresentação

O projeto é um jogo educativo de verificação de notícias. O usuário informa seus dados, escolhe temas de interesse e responde se cada manchete é fato ou fake.

O objetivo é exercitar lógica de programação, estruturação de código, integração entre módulos e uso de interface gráfica em um contexto de educação digital.

## Objetivos do Projeto

- Desenvolver uma aplicação interativa em Python.
- Aplicar conceitos de controle de fluxo, funções, listas e organização modular.
- Explorar interface gráfica com `PySide6`.
- Armazenar participantes, partidas, respostas e ranking em banco local.
- Exibir feedback educativo após cada resposta.

## Fluxo da Aplicação

1. Tela inicial com nome, idade, consentimento e temas de interesse.
2. Tela de quiz com manchete, contexto e botões `É FATO` e `É FAKE`.
3. Tela de feedback com explicação da resposta.
4. Tela final com pontuação.
5. Tela de ranking com histórico das partidas.

## Estrutura do Projeto

```text
trabalho_final_ip_laboratoriofakenews---equipe-ednAI/
├── main.py
├── requirements.txt
├── backend/
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
- documentação básica do projeto;

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

3. Inicie o backend:

```bash
python3 backend/app.py
```

4. Em outro terminal, com o ambiente virtual ativado, inicie a interface gráfica:

```bash
python3 main.py
```

Durante o quiz, a tela mostra um cronômetro e um contador de progresso no topo.

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

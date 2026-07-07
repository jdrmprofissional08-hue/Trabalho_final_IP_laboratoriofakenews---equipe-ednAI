# ednAI — Laboratório de Combate a Fake News (Interface Gráfica)

Este repositório contém a entrega da interface gráfica do software **ednAI - Laboratório de Combate a Fake News**, desenvolvido em Python utilizando **PySide6** como requisito para a disciplina de Introdução à Programação (UFCAT).

---

## 📌 Divisão do Trabalho - Grupo 2 (Front-end)

Este módulo foi projetado para separar de maneira limpa as responsabilidades de desenvolvimento da interface visual:

### Responsabilidades do Mateus (Desenvolvidas nesta entrega):
* **Identidade Visual**: Definição da paleta de cores moderna (Slate, Royal Blue, Emerald Green e Crimson Red), fontes do sistema limpas e folhas de estilo CSS/QSS.
* **Componentes Customizados**: Criação de painéis com sombra suave (`CardFrame`) e placeholders de imagens vetoriais desenhados via código (`ImagePlaceholder`) para máxima compatibilidade sem arquivos externos.
* **Tela Inicial**: Layout do formulário contendo Nome Completo, Idade (com validador numérico de entrada), seleção de temas de interesse via botões de seleção múltipla (grid responsivo) e aceite dos termos.
* **Tela do Quiz**: Cabeçalho de desafios, contador de progresso e porcentagem de forma síncrona, barra de progresso visual, estrutura do painel de notícias e botões estilizados "É FATO" e "É FAKE".
* **Garantia de Responsividade**: Utilização de layouts dinâmicos (`QVBoxLayout`, `QHBoxLayout`, `QGridLayout`) que garantem consistência visual tanto em computadores quanto em telas menores.

### Responsabilidades do Mouhamed (Estruturas prontas para integração):
* **Tela de Feedback**: Exibição da resposta do usuário com explicação educativa sobre a veracidade dos fatos. (Implementada como placeholder interativo).
* **Tela Final**: Painel de encerramento mostrando pontuação total de acertos e erros. (Implementada como placeholder interativo).
* **Tela de Ranking**: Classificação dos melhores jogadores da Mostra UFCAT. (Implementada como placeholder interativo integrado ao fluxo).

---

## 📁 Estrutura do Projeto

```
trabalho_ip_mateus/
│
├── main.py                     # Inicialização do Qt, orquestração e gerenciamento do fluxo do jogo
├── requirements.txt            # Dependência do framework PySide6
├── README.md                   # Documentação do projeto (este arquivo)
│
└── src/
    ├── __init__.py
    ├── styles.py               # Identidade visual, cores e master stylesheet QSS
    │
    └── ui/
        ├── __init__.py
        ├── components.py       # Cartões sombreados e placeholders vetoriais de mídia
        ├── tela_inicial.py     # Tela Inicial de Cadastro e Temas [Mateus]
        ├── tela_quiz.py        # Tela de Quiz de Verificação de Manchetes [Mateus]
        │
        # Placeholders estruturados prontos para a integração
        ├── tela_feedback.py    # Tela de feedback de acertos e justificativas
        ├── tela_final.py       # Tela de placar final
        └── tela_ranking.py     # Tela de ranking global da Mostra UFCAT
```

---

## 🚀 Como Executar o Projeto

Certifique-se de ter o Python 3.10 ou superior instalado em sua máquina.

### 1. Criar e ativar o ambiente virtual (Recomendado)

No terminal do seu sistema operacional (Windows PowerShell/CMD ou Linux/macOS):

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Ativar ambiente virtual (Windows CMD)
.\venv\Scripts\activate.bat

# Ativar ambiente virtual (Linux/macOS)
source venv/bin/activate
```

### 2. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 3. Iniciar a aplicação

```bash
python main.py
```

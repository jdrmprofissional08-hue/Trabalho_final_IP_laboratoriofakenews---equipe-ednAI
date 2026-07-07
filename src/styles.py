# -*- coding: utf-8 -*-

# Cores do Sistema
COLOR_PRIMARY = "#2563EB"       # Azul Royal
COLOR_PRIMARY_HOVER = "#1D4ED8" # Azul Escuro
COLOR_BACKGROUND = "#F8FAFC"    # Slate 50 (Fundo Geral)
COLOR_CARD = "#FFFFFF"          # Branco (Fundo de Containers)
COLOR_SUCCESS = "#10B981"       # Verde (É FATO)
COLOR_SUCCESS_HOVER = "#059669" # Verde Escuro
COLOR_SUCCESS_LIGHT = "#E6F4EA" # Verde Claro para Fundo
COLOR_SUCCESS_TEXT = "#137333"  # Verde Escuro para Texto
COLOR_DANGER = "#EF4444"        # Vermelho (É FAKE)
COLOR_DANGER_HOVER = "#DC2626"  # Vermelho Escuro
COLOR_DANGER_LIGHT = "#FCE8E6"  # Vermelho Claro para Fundo
COLOR_DANGER_TEXT = "#C5221F"   # Vermelho Escuro para Texto
COLOR_TEXT_PRIMARY = "#1E293B"  # Slate 800 (Texto Principal)
COLOR_TEXT_SECONDARY = "#64748B"# Slate 500 (Texto Secundário)
COLOR_BORDER = "#E2E8F0"        # Slate 200 (Bordas)
COLOR_BORDER_FOCUS = "#3B82F6"  # Azul para Foco

# Imagem do Checkmark em Base64 SVG para uso direto no QSS
CHECKMARK_SVG_B64 = (
    "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9z"
    "dmciIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSJ3aGl0ZSIgc3Ryb2"
    "tlLXdpZHRoPSIzIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91"
    "bmQiPjxwb2x5bGluZSBwb2ludHM9IjIwIDYgOSAxNyA0IDEyIj48L3BvbHlsaW5lPjwvc3ZnPg=="
)

# Estilização QSS Geral da Aplicação
STYLE_SHEET = f"""
QMainWindow {{
    background-color: {COLOR_BACKGROUND};
}}

QWidget {{
    font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
    color: {COLOR_TEXT_PRIMARY};
}}

/* Card/Container com borda fina e cantos arredondados */
QFrame#CardFrame {{
    background-color: {COLOR_CARD};
    border: 1px solid {COLOR_BORDER};
    border-radius: 12px;
}}

/* Campo de Entrada de Texto */
QLineEdit {{
    background-color: {COLOR_CARD};
    border: 1px solid {COLOR_BORDER};
    border-radius: 8px;
    padding: 10px 14px;
    font-size: 14px;
    color: {COLOR_TEXT_PRIMARY};
}}
QLineEdit:focus {{
    border: 2px solid {COLOR_PRIMARY};
}}
QLineEdit:disabled {{
    background-color: #F1F5F9;
    color: #94A3B8;
    border-color: {COLOR_BORDER};
}}

/* Estilo de Rótulos */
QLabel#TitleLabel {{
    font-size: 26px;
    font-weight: bold;
    color: {COLOR_PRIMARY};
}}
QLabel#SubtitleLabel {{
    font-size: 14px;
    color: {COLOR_TEXT_SECONDARY};
}}
QLabel#SectionHeader {{
    font-size: 16px;
    font-weight: bold;
    color: {COLOR_TEXT_PRIMARY};
}}
QLabel#FieldLabel {{
    font-size: 13px;
    font-weight: bold;
    color: #475569;
}}

/* Botão Azul Geral */
QPushButton {{
    background-color: {COLOR_PRIMARY};
    color: #FFFFFF;
    border: none;
    border-radius: 8px;
    padding: 12px 24px;
    font-size: 14px;
    font-weight: bold;
}}
QPushButton:hover {{
    background-color: {COLOR_PRIMARY_HOVER};
}}
QPushButton:pressed {{
    background-color: #1E40AF;
}}
QPushButton:disabled {{
    background-color: #94A3B8;
    color: #E2E8F0;
}}

/* Botão de Categoria (Toggle) */
QPushButton#CategoryBtn {{
    background-color: {COLOR_CARD};
    color: {COLOR_TEXT_PRIMARY};
    border: 1px solid {COLOR_BORDER};
    border-radius: 8px;
    padding: 12px;
    text-align: left;
    font-size: 14px;
    font-weight: 500;
}}
QPushButton#CategoryBtn:hover {{
    background-color: #F1F5F9;
    border-color: #CBD5E1;
}}
QPushButton#CategoryBtn:checked {{
    background-color: #EFF6FF;
    border: 2px solid {COLOR_PRIMARY};
    color: {COLOR_PRIMARY};
}}

/* Botão É FATO */
QPushButton#btnFato {{
    background-color: {COLOR_SUCCESS_LIGHT};
    color: {COLOR_SUCCESS_TEXT};
    border: 2px solid {COLOR_SUCCESS_TEXT};
    border-radius: 8px;
    font-size: 16px;
    font-weight: bold;
    padding: 14px;
}}
QPushButton#btnFato:hover {{
    background-color: #CEEAD6;
}}
QPushButton#btnFato:pressed {{
    background-color: #A7F3D0;
}}

/* Botão É FAKE */
QPushButton#btnFake {{
    background-color: {COLOR_DANGER_LIGHT};
    color: {COLOR_DANGER_TEXT};
    border: 2px solid {COLOR_DANGER_TEXT};
    border-radius: 8px;
    font-size: 16px;
    font-weight: bold;
    padding: 14px;
}}
QPushButton#btnFake:hover {{
    background-color: #FAD2CF;
}}
QPushButton#btnFake:pressed {{
    background-color: #F87171;
}}

/* Barra de Progresso */
QProgressBar {{
    background-color: {COLOR_BORDER};
    border: none;
    border-radius: 4px;
    height: 8px;
}}
QProgressBar::chunk {{
    background-color: {COLOR_PRIMARY};
    border-radius: 4px;
}}

/* Checkbox Customizado */
QCheckBox {{
    font-size: 13px;
    color: #475569;
    spacing: 8px;
}}
QCheckBox::indicator {{
    width: 18px;
    height: 18px;
    border: 1px solid #CBD5E1;
    border-radius: 4px;
    background-color: {COLOR_CARD};
}}
QCheckBox::indicator:unchecked:hover {{
    border-color: {COLOR_TEXT_SECONDARY};
}}
QCheckBox::indicator:checked {{
    background-color: {COLOR_PRIMARY};
    border-color: {COLOR_PRIMARY};
    image: url('{CHECKMARK_SVG_B64}');
}}
"""

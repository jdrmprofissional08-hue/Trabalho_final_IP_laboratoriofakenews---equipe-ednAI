# -*- coding: utf-8 -*-

import re

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QSpacerItem, QSizePolicy, QFrame, QTextEdit, QLineEdit
)
from PySide6.QtCore import Signal, Qt
from src.ui.components import CardFrame

class TelaFinal(QWidget):
    jogar_novamente_signal = Signal()
    ver_ranking_signal = Signal()
    perguntar_ednai_signal = Signal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        
    def init_ui(self):
        # Layout Principal (Vertical)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 30, 40, 30)
        main_layout.setSpacing(18)
        main_layout.setAlignment(Qt.AlignHCenter)
        
        # --- HEADER ---
        header_layout = QVBoxLayout()
        header_layout.setSpacing(5)
        header_layout.setAlignment(Qt.AlignCenter)
        
        lbl_fase = QLabel("🏁 FIM DE JOGO")
        lbl_fase.setAlignment(Qt.AlignCenter)
        lbl_fase.setStyleSheet("font-size: 11px; font-weight: bold; color: #DC2626; background-color: #FEE2E2; padding: 4px 10px; border-radius: 12px;")
        
        lbl_title = QLabel("Resultados do Laboratório")
        lbl_title.setObjectName("TitleLabel")
        lbl_title.setAlignment(Qt.AlignCenter)
        
        header_layout.addWidget(lbl_fase, 0, Qt.AlignHCenter)
        header_layout.addWidget(lbl_title)
        main_layout.addLayout(header_layout)
        
        # --- CARD DE PONTOS ---
        self.card = CardFrame()
        self.card.setMaximumWidth(580)
        card_layout = QVBoxLayout(self.card)
        card_layout.setContentsMargins(30, 30, 30, 30)
        card_layout.setSpacing(16)
        card_layout.setAlignment(Qt.AlignCenter)
        
        lbl_pont_title = QLabel("SUA PONTUAÇÃO")
        lbl_pont_title.setStyleSheet("font-size: 13px; font-weight: bold; color: #64748B; letter-spacing: 1px;")
        lbl_pont_title.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(lbl_pont_title)
        
        self.lbl_pontos = QLabel("8 / 10")
        self.lbl_pontos.setStyleSheet("font-size: 48px; font-weight: 800; color: #2563EB;")
        self.lbl_pontos.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(self.lbl_pontos)
        
        self.lbl_detalhes = QLabel("Acertos: 8   |   Erros: 2")
        self.lbl_detalhes.setStyleSheet("font-size: 15px; font-weight: 600; color: #475569;")
        self.lbl_detalhes.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(self.lbl_detalhes)
        
        # Divider Line
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("background-color: #E2E8F0; max-height: 1px; border: none;")
        card_layout.addWidget(line)
        
        self.lbl_feedback = QLabel(
            "Parabéns! Você tem um ótimo faro contra notícias falsas. "
            "Continue questionando o que lê na internet."
        )
        self.lbl_feedback.setStyleSheet("font-size: 14px; color: #64748B; line-height: 1.5;")
        self.lbl_feedback.setWordWrap(True)
        self.lbl_feedback.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(self.lbl_feedback)
        
        main_layout.addWidget(self.card)

        # --- CARD EDNAI ---
        self.card_ednai = CardFrame()
        self.card_ednai.setMaximumWidth(580)
        ednai_layout = QVBoxLayout(self.card_ednai)
        ednai_layout.setContentsMargins(20, 18, 20, 18)
        ednai_layout.setSpacing(10)

        lbl_ednai = QLabel("🤖 Ednai")
        lbl_ednai.setStyleSheet("font-size: 13px; font-weight: bold; color: #2563EB;")
        ednai_layout.addWidget(lbl_ednai)

        self.txt_ednai = QTextEdit()
        self.txt_ednai.setReadOnly(True)
        self.txt_ednai.setMaximumHeight(150)
        self.txt_ednai.setPlaceholderText("A análise do Ednai aparecerá aqui após o fim do desafio.")
        self.txt_ednai.setStyleSheet(
            "background-color: #F8FAFC; border: 1px solid #E2E8F0; "
            "border-radius: 8px; padding: 8px; font-size: 13px;"
        )
        ednai_layout.addWidget(self.txt_ednai)

        pergunta_layout = QHBoxLayout()
        pergunta_layout.setSpacing(8)
        self.txt_pergunta_ednai = QLineEdit()
        self.txt_pergunta_ednai.setPlaceholderText("Pergunte ao Ednai sobre seu resultado...")
        self.txt_pergunta_ednai.returnPressed.connect(self._emitir_pergunta_ednai)

        self.btn_perguntar_ednai = QPushButton("Perguntar")
        self.btn_perguntar_ednai.setCursor(Qt.PointingHandCursor)
        self.btn_perguntar_ednai.clicked.connect(self._emitir_pergunta_ednai)

        pergunta_layout.addWidget(self.txt_pergunta_ednai)
        pergunta_layout.addWidget(self.btn_perguntar_ednai)
        ednai_layout.addLayout(pergunta_layout)
        main_layout.addWidget(self.card_ednai)
        
        # --- BOTÕES DE NAVEGAÇÃO ---
        botoes_layout = QHBoxLayout()
        botoes_layout.setSpacing(15)
        #botoes_layout.setMaximumWidth(580)
        
        self.btn_ranking = QPushButton("🏆 Ver Ranking")
        self.btn_ranking.setCursor(Qt.PointingHandCursor)
        self.btn_ranking.setStyleSheet("background-color: #FFFFFF; color: #2563EB; border: 1px solid #2563EB; padding: 12px;")
        self.btn_ranking.clicked.connect(lambda: self.ver_ranking_signal.emit())

        self.btn_novo_jogo = QPushButton("Jogar Novamente  ➔")
        self.btn_novo_jogo.setCursor(Qt.PointingHandCursor)
        self.btn_novo_jogo.clicked.connect(lambda: self.jogar_novamente_signal.emit())
        
        botoes_layout.addWidget(self.btn_ranking)
        botoes_layout.addWidget(self.btn_novo_jogo)
        main_layout.addLayout(botoes_layout)
        
        # --- FOOTER ---
        main_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))
        lbl_footer = QLabel("ednAI • Introdução à Programação • UFCAT")
        lbl_footer.setAlignment(Qt.AlignCenter)
        lbl_footer.setStyleSheet("font-size: 11px; color: #94A3B8; font-weight: 500;")
        main_layout.addWidget(lbl_footer)
        
    def exibir_resultados(self, acertos, total):
        """Atualiza a pontuação exibida."""
        self.lbl_pontos.setText(f"{acertos} / {total}")
        erros = total - acertos
        self.lbl_detalhes.setText(f"Acertos: {acertos}   |   Erros: {erros}")
        self.txt_ednai.clear()
        self.txt_pergunta_ednai.clear()
        self.btn_perguntar_ednai.setEnabled(False)
        self.btn_perguntar_ednai.setText("Perguntar")
        
        taxa = acertos / total if total > 0 else 0
        if taxa == 1.0:
            self.lbl_feedback.setText("Perfeito! Você desmascarou todas as notícias falsas. Um verdadeiro perito digital!")
        elif taxa >= 0.7:
            self.lbl_feedback.setText("Muito bom! Você tem um ótimo faro contra notícias falsas.")
        elif taxa >= 0.5:
            self.lbl_feedback.setText("Bom resultado, mas fique atento. Algumas desinformações conseguiram te enganar.")
        else:
            self.lbl_feedback.setText("Cuidado! As notícias falsas te enganaram na maioria das vezes. Treine mais seu olhar crítico.")

    def exibir_ednai_carregando(self):
        self.txt_ednai.setPlainText("Ednai está analisando seu desempenho...")
        self.btn_perguntar_ednai.setEnabled(False)

    def exibir_ednai_resposta(self, resposta):
        self.txt_ednai.setPlainText(self._limpar_texto_ednai(resposta))
        self.txt_pergunta_ednai.clear()
        self.btn_perguntar_ednai.setEnabled(True)
        self.btn_perguntar_ednai.setText("Perguntar")

    def exibir_ednai_erro(self, mensagem):
        self.txt_ednai.setPlainText(mensagem)
        self.btn_perguntar_ednai.setEnabled(True)
        self.btn_perguntar_ednai.setText("Perguntar")

    def exibir_ednai_pergunta_em_andamento(self):
        self.btn_perguntar_ednai.setEnabled(False)
        self.btn_perguntar_ednai.setText("Analisando...")

    def _emitir_pergunta_ednai(self):
        pergunta = self.txt_pergunta_ednai.text().strip()
        if pergunta:
            self.perguntar_ednai_signal.emit(pergunta)

    def _limpar_texto_ednai(self, texto):
        texto = str(texto or "").strip()
        texto = re.sub(r"```[a-zA-Z0-9_-]*", "", texto)
        texto = texto.replace("```", "")
        texto = re.sub(r"^\s{0,3}#{1,6}\s*", "", texto, flags=re.MULTILINE)
        texto = re.sub(r"^\s{0,3}>\s?", "", texto, flags=re.MULTILINE)
        texto = re.sub(r"(\*\*|__|\*)", "", texto)
        texto = re.sub(r"^\s*[-+]\s+", "• ", texto, flags=re.MULTILINE)
        texto = re.sub(r"[“”]", '"', texto)
        texto = re.sub(r"[‘’]", "'", texto)
        texto = re.sub(r"\n{3,}", "\n\n", texto)

        if len(texto) >= 2 and texto[0] == texto[-1] and texto[0] in {'"', "'"}:
            texto = texto[1:-1].strip()

        return texto

# -*- coding: utf-8 -*-

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QSpacerItem, QSizePolicy, QFrame
)
from PySide6.QtCore import Signal, Qt
from src.ui.components import CardFrame

class TelaFinal(QWidget):
    jogar_novamente_signal = Signal()
    ver_ranking_signal = Signal()
    
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
            "Parabéns! Você tem um ótimo faro contra notícias falsas geradas por IA. "
            "Continue questionando o que lê na internet."
        )
        self.lbl_feedback.setStyleSheet("font-size: 14px; color: #64748B; line-height: 1.5;")
        self.lbl_feedback.setWordWrap(True)
        self.lbl_feedback.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(self.lbl_feedback)
        
        main_layout.addWidget(self.card)
        
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
        
        taxa = acertos / total if total > 0 else 0
        if taxa == 1.0:
            self.lbl_feedback.setText("Perfeito! Você desmascarou todas as notícias falsas. Um verdadeiro perito digital!")
        elif taxa >= 0.7:
            self.lbl_feedback.setText("Muito bom! Você tem um ótimo faro contra notícias falsas geradas por IA.")
        elif taxa >= 0.5:
            self.lbl_feedback.setText("Bom resultado, mas fique atento. Algumas desinformações geradas por IA conseguiram te enganar.")
        else:
            self.lbl_feedback.setText("Cuidado! As notícias falsas geradas por IA te enganaram na maioria das vezes. Treine mais seu olhar crítico.")

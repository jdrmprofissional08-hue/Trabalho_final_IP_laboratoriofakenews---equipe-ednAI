# -*- coding: utf-8 -*-

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, 
    QPushButton, QSpacerItem, QSizePolicy, QFrame
)
from PySide6.QtCore import Signal, Qt
from src.ui.components import CardFrame

class TelaFeedback(QWidget):
    # Sinal disparado para seguir adiante (próxima pergunta ou final)
    proxima_pergunta_signal = Signal()
    
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
        
        lbl_fase = QLabel("✨ FEEDBACK EDUCATIVO")
        lbl_fase.setAlignment(Qt.AlignCenter)
        lbl_fase.setStyleSheet("font-size: 11px; font-weight: bold; color: #64748B; background-color: #E2E8F0; padding: 4px 10px; border-radius: 12px;")
        
        header_layout.addWidget(lbl_fase, 0, Qt.AlignHCenter)
        main_layout.addLayout(header_layout)
        
        # --- TÍTULO DO ACERTO/ERRO ---
        self.lbl_resultado = QLabel("Você Acertou!")
        self.lbl_resultado.setAlignment(Qt.AlignCenter)
        self.lbl_resultado.setStyleSheet("font-size: 26px; font-weight: bold; color: #10B981;") # Verde padrão
        main_layout.addWidget(self.lbl_resultado)
        
        # --- CARD DE EXPLICAÇÃO ---
        self.card = CardFrame()
        self.card.setMaximumWidth(580)
        card_layout = QVBoxLayout(self.card)
        card_layout.setContentsMargins(25, 25, 25, 25)
        card_layout.setSpacing(14)
        
        lbl_exp_header = QLabel("💡 POR QUE ESSA DECISÃO?")
        lbl_exp_header.setStyleSheet("font-size: 13px; font-weight: bold; color: #2563EB; letter-spacing: 0.5px;")
        card_layout.addWidget(lbl_exp_header)
        
        self.lbl_explicacao = QLabel(
            "Esta notícia foi classificada como FAKE porque apresenta sinais de desinformação "
            "e afirmações que não constam em fontes confiáveis."
        )
        self.lbl_explicacao.setStyleSheet("font-size: 14px; color: #1E293B; line-height: 1.5;")
        self.lbl_explicacao.setWordWrap(True)
        card_layout.addWidget(self.lbl_explicacao)
        
        # Divider Line
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("background-color: #E2E8F0; max-height: 1px; border: none;")
        card_layout.addWidget(line)
        
        # Fonte de verificação
        fonte_header = QLabel("🔗 FONTE CONFIÁVEL DE CHECAGEM")
        fonte_header.setStyleSheet("font-size: 11px; font-weight: bold; color: #64748B; letter-spacing: 0.5px;")
        card_layout.addWidget(fonte_header)
        
        self.lbl_link = QLabel('<a href="https://www.ufcat.edu.br" style="color: #2563EB; text-decoration: none; font-weight: bold;">Fato ou Fake - Acesse o site do projeto para saber mais</a>')
        self.lbl_link.setOpenExternalLinks(True)
        self.lbl_link.setStyleSheet("font-size: 13px;")
        card_layout.addWidget(self.lbl_link)
        
        main_layout.addWidget(self.card)
        
        # --- BOTÃO PROSSEGUIR ---
        self.btn_proximo = QPushButton("Próxima Pergunta  ➔")
        self.btn_proximo.setObjectName("btnProximo")
        self.btn_proximo.setCursor(Qt.PointingHandCursor)
        self.btn_proximo.setMaximumWidth(580)
        self.btn_proximo.clicked.connect(lambda: self.proxima_pergunta_signal.emit())
        main_layout.addWidget(self.btn_proximo)
        
        # --- FOOTER ---
        main_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))
        lbl_footer = QLabel("ednAI • Introdução à Programação • UFCAT")
        lbl_footer.setAlignment(Qt.AlignCenter)
        lbl_footer.setStyleSheet("font-size: 11px; color: #94A3B8; font-weight: 500;")
        main_layout.addWidget(lbl_footer)
        
    def exibir_feedback(self, acertou, explicacao_texto, link_texto, link_url, eh_ultima=False):
        """Preenche a tela com os resultados da resposta."""
        if acertou:
            self.lbl_resultado.setText("🎉 Você Acertou!")
            self.lbl_resultado.setStyleSheet("font-size: 26px; font-weight: bold; color: #10B981;")
        else:
            self.lbl_resultado.setText("❌ Você Errou!")
            self.lbl_resultado.setStyleSheet("font-size: 26px; font-weight: bold; color: #EF4444;")
            
        self.lbl_explicacao.setText(explicacao_texto)
        self.lbl_link.setText(f'<a href="{link_url}" style="color: #2563EB; text-decoration: none; font-weight: bold;">{link_texto}</a>')
        
        if eh_ultima:
            self.btn_proximo.setText("Ver Resultados Finais  ➔")
        else:
            self.btn_proximo.setText("Próxima Pergunta  ➔")

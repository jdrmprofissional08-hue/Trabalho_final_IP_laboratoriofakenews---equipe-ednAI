# -*- coding: utf-8 -*-

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QFrame, QSpacerItem, QSizePolicy
)
from PySide6.QtCore import Signal, Qt
from src.ui.components import CardFrame

class TelaRanking(QWidget):
    voltar_inicio_signal = Signal()
    
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
        
        lbl_fase = QLabel("🏆 QUADRO DE HONRA")
        lbl_fase.setAlignment(Qt.AlignCenter)
        lbl_fase.setStyleSheet("font-size: 11px; font-weight: bold; color: #D97706; background-color: #FEF3C7; padding: 4px 10px; border-radius: 12px;")
        
        lbl_title = QLabel("Ranking Geral")
        lbl_title.setObjectName("TitleLabel")
        lbl_title.setAlignment(Qt.AlignCenter)
        
        lbl_sub = QLabel("Mostra UFCAT — Atualização ao vivo")
        lbl_sub.setObjectName("SubtitleLabel")
        lbl_sub.setAlignment(Qt.AlignCenter)
        
        header_layout.addWidget(lbl_fase, 0, Qt.AlignHCenter)
        header_layout.addWidget(lbl_title)
        header_layout.addWidget(lbl_sub)
        main_layout.addLayout(header_layout)
        
        # --- CARD DO RANKING ---
        self.card = CardFrame()
        self.card.setMaximumWidth(580)
        self.card_layout = QVBoxLayout(self.card)
        self.card_layout.setContentsMargins(25, 25, 25, 25)
        self.card_layout.setSpacing(10)
        
        # Cabeçalho da tabela
        tbl_header = QHBoxLayout()
        tbl_header.setContentsMargins(10, 0, 10, 5)
        
        lbl_col_pos = QLabel("POSIÇÃO")
        lbl_col_pos.setStyleSheet("font-size: 11px; font-weight: bold; color: #94A3B8; letter-spacing: 0.5px;")
        lbl_col_pos.setFixedWidth(80)
        
        lbl_col_nome = QLabel("NOME")
        lbl_col_nome.setStyleSheet("font-size: 11px; font-weight: bold; color: #94A3B8; letter-spacing: 0.5px;")
        
        lbl_col_pont = QLabel("PONTUAÇÃO")
        lbl_col_pont.setStyleSheet("font-size: 11px; font-weight: bold; color: #94A3B8; letter-spacing: 0.5px;")
        lbl_col_pont.setAlignment(Qt.AlignRight)
        lbl_col_pont.setFixedWidth(100)
        
        tbl_header.addWidget(lbl_col_pos)
        tbl_header.addWidget(lbl_col_nome)
        tbl_header.addWidget(lbl_col_pont)
        self.card_layout.addLayout(tbl_header)
        
        # Container para os itens de dados
        self.rows_layout = QVBoxLayout()
        self.rows_layout.setSpacing(8)
        self.card_layout.addLayout(self.rows_layout)
        
        main_layout.addWidget(self.card)
        
        # Preenche com dados mockados inicialmente
        self.carregar_ranking_mock()
        
        # --- BOTÃO VOLTAR ---
        self.btn_voltar = QPushButton("Voltar para o Início")
        self.btn_voltar.setCursor(Qt.PointingHandCursor)
        self.btn_voltar.setMaximumWidth(580)
        self.btn_voltar.clicked.connect(lambda: self.voltar_inicio_signal.emit())
        main_layout.addWidget(self.btn_voltar)
        
        # --- FOOTER ---
        main_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))
        lbl_footer = QLabel("ednAI • Introdução à Programação • UFCAT")
        lbl_footer.setAlignment(Qt.AlignCenter)
        lbl_footer.setStyleSheet("font-size: 11px; color: #94A3B8; font-weight: 500;")
        main_layout.addWidget(lbl_footer)
        
    def carregar_ranking_mock(self):
        """Carrega uma lista simulada de jogadores do ranking."""
        mock_data = [
            {"nome": "Júlia Mendes", "pontos": "10/10"},
            {"nome": "Rafael Costa", "pontos": "9/10"},
            {"nome": "Bianca Oliveira", "pontos": "9/10"},
            {"nome": "Lucas Pereira", "pontos": "8/10"},
            {"nome": "Marina Alves", "pontos": "7/10"},
        ]
        self.definir_dados_ranking(mock_data)
        
    def definir_dados_ranking(self, lista_jogadores):
        """Limpa o ranking atual e desenha os novos dados recebidos do backend."""
        # Limpar layout antigo
        while self.rows_layout.count():
            item = self.rows_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
                
        # Desenhar novas linhas
        for idx, jogador in enumerate(lista_jogadores):
            posicao = idx + 1
            nome = jogador.get("nome", "Sem Nome")
            pontos = jogador.get("pontos", "0")
            
            row_frame = QFrame()
            row_frame.setObjectName("RankingRow")
            
            # Estilos de linha
            bg_color = "#FFFFFF"
            border_style = "border: 1px solid #E2E8F0;"
            
            # Linhas com cores de fundo especiais para os 3 primeiros
            if posicao == 1:
                bg_color = "#FEF3C7"  # Dourado claro
                border_style = "border: 1px solid #FCD34D;"
                pos_text = "🥇  #1"
            elif posicao == 2:
                bg_color = "#F1F5F9"  # Prata claro
                border_style = "border: 1px solid #E2E8F0;"
                pos_text = "🥈  #2"
            elif posicao == 3:
                bg_color = "#FAF7F2"  # Bronze claro (laranja bem claro)
                border_style = "border: 1px solid #FFEDD5;"
                pos_text = "🥉  #3"
            else:
                pos_text = f"     #{posicao}"
                
            row_frame.setStyleSheet(
                f"QFrame {{ background-color: {bg_color}; {border_style} border-radius: 8px; }}"
            )
            
            row_layout = QHBoxLayout(row_frame)
            row_layout.setContentsMargins(15, 12, 15, 12)
            
            lbl_pos = QLabel(pos_text)
            lbl_pos.setStyleSheet("font-size: 13px; font-weight: bold; color: #1E293B;")
            lbl_pos.setFixedWidth(80)
            
            lbl_nome = QLabel(nome)
            lbl_nome.setStyleSheet("font-size: 13px; font-weight: 600; color: #1E293B;")
            
            lbl_pont = QLabel(pontos)
            lbl_pont.setStyleSheet("font-size: 13px; font-weight: bold; color: #2563EB;")
            lbl_pont.setAlignment(Qt.AlignRight)
            lbl_pont.setFixedWidth(100)
            
            row_layout.addWidget(lbl_pos)
            row_layout.addWidget(lbl_nome)
            row_layout.addWidget(lbl_pont)
            
            self.rows_layout.addWidget(row_frame)

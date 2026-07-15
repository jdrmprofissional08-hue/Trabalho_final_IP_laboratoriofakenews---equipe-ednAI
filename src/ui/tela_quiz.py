# -*- coding: utf-8 -*-

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QProgressBar, QSpacerItem, QSizePolicy
)
from PySide6.QtCore import Signal, Qt
from src.ui.components import CardFrame, ImagePlaceholder

class TelaQuiz(QWidget):
    # Sinal disparado quando o usuário responde (True = FATO, False = FAKE)
    resposta_signal = Signal(bool)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.pergunta_atual_dados = None
        self.init_ui()
        
    def init_ui(self):
        # Layout Principal da Tela (Vertical)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(24, 16, 24, 16)
        main_layout.setSpacing(10)
        main_layout.setAlignment(Qt.AlignHCenter)
        
        # --- HEADER DE FASE ---
        header_layout = QVBoxLayout()
        header_layout.setSpacing(2)
        header_layout.setAlignment(Qt.AlignCenter)
        
        lbl_fase = QLabel("✨ FASE 02")
        lbl_fase.setAlignment(Qt.AlignCenter)
        lbl_fase.setStyleSheet("font-size: 11px; font-weight: bold; color: #2563EB; background-color: #EFF6FF; padding: 4px 10px; border-radius: 12px;")
        
        lbl_title = QLabel("Desafio de Verificação")
        lbl_title.setObjectName("TitleLabel")
        lbl_title.setAlignment(Qt.AlignCenter)
        
        lbl_sub = QLabel("Leia cuidadosamente a postagem abaixo e decida: trata-se de um fato verídico ou uma fake news?")
        lbl_sub.setObjectName("SubtitleLabel")
        lbl_sub.setAlignment(Qt.AlignCenter)
        
        header_layout.addWidget(lbl_fase, 0, Qt.AlignHCenter)
        header_layout.addWidget(lbl_title)
        header_layout.addWidget(lbl_sub)
        main_layout.addLayout(header_layout)
        
        # --- CONTAINER DE PROGRESSO ---
        prog_container = QVBoxLayout()
        prog_container.setSpacing(4)
        #prog_container.setMaximumWidth(580)

        # Barra superior com tempo e progresso
        topo_layout = QHBoxLayout()
        topo_layout.setSpacing(12)

        self.lbl_tempo = QLabel("⏱ 00:00")
        self.lbl_tempo.setStyleSheet(
            "font-size: 12px; font-weight: bold; color: #0F172A; "
            "background-color: #E0F2FE; padding: 4px 10px; border-radius: 999px;"
        )

        self.lbl_status = QLabel("📰 0/10")
        self.lbl_status.setStyleSheet(
            "font-size: 12px; font-weight: bold; color: #0F172A; "
            "background-color: #EEF2FF; padding: 4px 10px; border-radius: 999px;"
        )
        self.lbl_status.setAlignment(Qt.AlignCenter)

        topo_layout.addWidget(self.lbl_tempo, 0, Qt.AlignLeft)
        topo_layout.addStretch(1)
        topo_layout.addWidget(self.lbl_status, 0, Qt.AlignRight)
        prog_container.addLayout(topo_layout)
        
        # Labels de texto (Número da Pergunta e Percentual)
        labels_layout = QHBoxLayout()
        self.lbl_contador = QLabel("Pergunta 1 de 5")
        self.lbl_contador.setStyleSheet("font-size: 13px; font-weight: bold; color: #475569;")
        
        self.lbl_percentual = QLabel("20% concluído")
        self.lbl_percentual.setStyleSheet("font-size: 13px; font-weight: 500; color: #64748B;")
        self.lbl_percentual.setAlignment(Qt.AlignRight)
        
        labels_layout.addWidget(self.lbl_contador)
        labels_layout.addWidget(self.lbl_percentual)
        prog_container.addLayout(labels_layout)
        
        # Barra de Progresso
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(20)
        self.progress_bar.setTextVisible(False)
        prog_container.addWidget(self.progress_bar)
        
        main_layout.addLayout(prog_container)
        
        # --- CARD DA NOTÍCIA (POSTAGEM) ---
        self.card = CardFrame()
        self.card.setMaximumWidth(640)
        card_layout = QVBoxLayout(self.card)
        card_layout.setContentsMargins(18, 18, 18, 18)
        card_layout.setSpacing(10)
        
        # Placeholder de Imagem
        self.image_widget = ImagePlaceholder("IMAGEM DA POSTAGEM")
        card_layout.addWidget(self.image_widget)
        
        # Fonte / Data da Notícia
        self.lbl_fonte = QLabel("PORTAL NOTÍCIAS HOJE • há 2 horas")
        self.lbl_fonte.setStyleSheet("font-size: 10px; font-weight: bold; color: #2563EB; text-transform: uppercase; letter-spacing: 0.4px;")
        card_layout.addWidget(self.lbl_fonte)
        
        # Manchete/Título
        self.lbl_manchete = QLabel("Título da Manchete da Notícia Fato ou Fake")
        self.lbl_manchete.setStyleSheet("font-size: 17px; font-weight: bold; color: #1E293B; line-height: 1.2;")
        self.lbl_manchete.setWordWrap(True)
        card_layout.addWidget(self.lbl_manchete)
        
        # Contexto/Descrição
        self.lbl_contexto = QLabel(
            "Texto de contexto contendo detalhes da notícia que podem dar dicas se ela "
            "é verídica ou se é uma desinformação."
        )
        self.lbl_contexto.setStyleSheet("font-size: 13px; color: #475569; line-height: 1.35;")
        self.lbl_contexto.setWordWrap(True)
        card_layout.addWidget(self.lbl_contexto)
        
        main_layout.addWidget(self.card)
        
        # --- BOTÕES DE DECISÃO ---
        botoes_layout = QHBoxLayout()
        botoes_layout.setSpacing(10)
        #botoes_layout.setMaximumWidth(580)
        
        self.btn_fato = QPushButton("✔  É FATO")
        self.btn_fato.setObjectName("btnFato")
        self.btn_fato.setCursor(Qt.PointingHandCursor)
        self.btn_fato.clicked.connect(lambda: self._emitir_resposta(True))
        
        self.btn_fake = QPushButton("✖  É FAKE")
        self.btn_fake.setObjectName("btnFake")
        self.btn_fake.setCursor(Qt.PointingHandCursor)
        self.btn_fake.clicked.connect(lambda: self._emitir_resposta(False))
        
        botoes_layout.addWidget(self.btn_fato)
        botoes_layout.addWidget(self.btn_fake)
        main_layout.addLayout(botoes_layout)
        
        # --- ESPAÇADOR E FOOTER ---
        main_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        lbl_footer = QLabel("ednAI • Introdução à Programação • UFCAT")
        lbl_footer.setAlignment(Qt.AlignCenter)
        lbl_footer.setStyleSheet("font-size: 10px; color: #94A3B8; font-weight: 500;")
        main_layout.addWidget(lbl_footer)
        
    def carregar_pergunta(self, pergunta_dados):
        """Atualiza a interface com os dados de uma nova pergunta."""
        self.pergunta_atual_dados = pergunta_dados
        self.definir_botoes_resposta_habilitados(True)
        self.lbl_fonte.setText(f"{pergunta_dados.get('fonte', 'PORTAL NOTÍCIAS')} • {pergunta_dados.get('tempo', 'recentemente')}")
        self.lbl_manchete.setText(pergunta_dados.get('manchete', ''))
        self.lbl_contexto.setText(pergunta_dados.get('texto', ''))
        
        # Define o tema do placeholder da imagem
        tema = pergunta_dados.get('tema', 'NOTÍCIA')
        self.image_widget.text = f"IMAGEM SOBRE: {tema.upper()}"
        self.image_widget.image_path = pergunta_dados.get("image_path", "")
        self.image_widget.update() # Força redesenho
        
    def atualizar_progresso(self, atual, total):
        """Atualiza o contador textual e a barra de progresso."""
        self.lbl_contador.setText(f"Pergunta {atual} de {total}")
        self.lbl_status.setText(f"📰 {atual}/{total}")
        percentual = int((atual / total) * 100) if total > 0 else 0
        self.lbl_percentual.setText(f"{percentual}% concluído")
        self.progress_bar.setValue(percentual)

    def atualizar_tempo(self, segundos):
        minutos = max(0, segundos) // 60
        restante = max(0, segundos) % 60
        self.lbl_tempo.setText(f"⏱ {minutos:02d}:{restante:02d}")

    def definir_botoes_resposta_habilitados(self, habilitado):
        self.btn_fato.setEnabled(habilitado)
        self.btn_fake.setEnabled(habilitado)

    def _emitir_resposta(self, resposta):
        self.definir_botoes_resposta_habilitados(False)
        self.resposta_signal.emit(resposta)

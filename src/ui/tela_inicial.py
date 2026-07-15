# -*- coding: utf-8 -*-

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, 
    QPushButton, QCheckBox, QGridLayout, QSpacerItem, QSizePolicy
)
from PySide6.QtGui import QIntValidator
from PySide6.QtCore import Signal, Qt
from src.ui.components import CardFrame

class TelaInicial(QWidget):
    # Sinal disparado quando o usuário clica em "Iniciar Laboratório" com os dados do form
    iniciar_jogo_signal = Signal(dict)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        
    def init_ui(self):
        # Layout Principal da Tela (Vertical)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 30, 40, 30)
        main_layout.setSpacing(15)
        main_layout.setAlignment(Qt.AlignHCenter)
        
        # --- HEADER ---
        header_layout = QVBoxLayout()
        header_layout.setSpacing(5)
        
        lbl_inst = QLabel("UFCAT")
        lbl_inst.setAlignment(Qt.AlignCenter)
        lbl_inst.setStyleSheet("font-size: 11px; font-weight: bold; color: #94A3B8; letter-spacing: 1px;")
        
        lbl_title = QLabel("Laboratório de Combate a Fake News")
        lbl_title.setObjectName("TitleLabel")
        lbl_title.setAlignment(Qt.AlignCenter)
        
        lbl_sub = QLabel(
            "Coloque seu olhar crítico à prova. As notícias neste laboratório foram\n"
            "selecionadas para testar sua capacidade de distinguir o\n"
            "que é fato do que é fake."
        )
        lbl_sub.setObjectName("SubtitleLabel")
        lbl_sub.setAlignment(Qt.AlignCenter)
        
        header_layout.addWidget(lbl_inst)
        header_layout.addWidget(lbl_title)
        header_layout.addWidget(lbl_sub)
        main_layout.addLayout(header_layout)
        
        # --- CARD CENTRAL DE FORMULÁRIO ---
        self.card = CardFrame()
        card_layout = QVBoxLayout(self.card)
        card_layout.setContentsMargins(30, 25, 30, 25)
        card_layout.setSpacing(18)
        
        # Subcabeçalho do Card
        lbl_ident = QLabel("🔍 IDENTIFICAÇÃO DO PARTICIPANTE")
        lbl_ident.setObjectName("SectionHeader")
        card_layout.addWidget(lbl_ident)
        
        # Campo: Nome Completo
        nome_layout = QVBoxLayout()
        nome_layout.setSpacing(6)
        lbl_nome = QLabel("Seu Nome completo")
        lbl_nome.setObjectName("FieldLabel")
        self.txt_nome = QLineEdit()
        self.txt_nome.setPlaceholderText("Ex: Maria Souza Lima")
        nome_layout.addWidget(lbl_nome)
        nome_layout.addWidget(self.txt_nome)
        card_layout.addLayout(nome_layout)
        
        # Campo: Idade
        idade_layout = QVBoxLayout()
        idade_layout.setSpacing(6)
        lbl_idade = QLabel("Idade")
        lbl_idade.setObjectName("FieldLabel")
        self.txt_idade = QLineEdit()
        self.txt_idade.setPlaceholderText("Ex: 21")
        # Apenas números entre 1 e 120
        self.txt_idade.setValidator(QIntValidator(1, 120))
        idade_layout.addWidget(lbl_idade)
        idade_layout.addWidget(self.txt_idade)
        card_layout.addLayout(idade_layout)
        
        # Seção de Temas de Interesse
        temas_header = QVBoxLayout()
        temas_header.setSpacing(4)
        lbl_temas_title = QLabel("📌 TEMAS DE INTERESSE")
        lbl_temas_title.setObjectName("SectionHeader")
        lbl_temas_sub = QLabel("Selecione os temas para personalizar as notícias da sua partida:")
        lbl_temas_sub.setObjectName("SubtitleLabel")
        temas_header.addWidget(lbl_temas_title)
        temas_header.addWidget(lbl_temas_sub)
        card_layout.addLayout(temas_header)
        
        # Grid 2x2 para Botões de Categoria (Toggle)
        grid_layout = QGridLayout()
        grid_layout.setSpacing(10)
        
        self.btn_esportes = QPushButton("⚽  Esportes e Suplementação")
        self.btn_saude = QPushButton("🎬  Cinema")
        self.btn_tecnologia = QPushButton("💻  Tecnologia")
        self.btn_ciencia = QPushButton("🔬  Ciência")
        
        self.temas_botoes = [self.btn_esportes, self.btn_saude, self.btn_tecnologia, self.btn_ciencia]
        
        for btn in self.temas_botoes:
            btn.setObjectName("CategoryBtn")
            btn.setCheckable(True)
            btn.setCursor(Qt.PointingHandCursor)
            # Conecta o sinal de toggle para revalidar o formulário
            btn.toggled.connect(self.validar_formulario)
            
        grid_layout.addWidget(self.btn_esportes, 0, 0)
        grid_layout.addWidget(self.btn_saude, 0, 1)
        grid_layout.addWidget(self.btn_tecnologia, 1, 0)
        grid_layout.addWidget(self.btn_ciencia, 1, 1)
        card_layout.addLayout(grid_layout)
        
        # Checkbox de Consentimento
        self.chk_consent = QCheckBox("Aceito que minha pontuação apareça no Ranking Geral")
        self.chk_consent.setCursor(Qt.PointingHandCursor)
        self.chk_consent.setChecked(True)  # Marcado por padrão
        card_layout.addWidget(self.chk_consent)
        
        # Botão Jogar
        self.btn_jogar = QPushButton("Iniciar Laboratório  ➔")
        self.btn_jogar.setCursor(Qt.PointingHandCursor)
        self.btn_jogar.setEnabled(False)  # Desabilitado até preenchimento correto
        self.btn_jogar.clicked.connect(self.ao_jogar_clicado)
        card_layout.addWidget(self.btn_jogar)
        
        # Adiciona o card ao layout principal com tamanho máximo de largura para ficar elegante
        self.card.setMaximumWidth(580)
        main_layout.addWidget(self.card)
        
        # Conecta as mudanças de texto dos inputs para validar dinamicamente
        self.txt_nome.textChanged.connect(self.validar_formulario)
        self.txt_idade.textChanged.connect(self.validar_formulario)
        
        # --- FOOTER ---
        main_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        lbl_footer = QLabel("ednAI • Introdução à Programação • UFCAT")
        lbl_footer.setAlignment(Qt.AlignCenter)
        lbl_footer.setStyleSheet("font-size: 11px; color: #94A3B8; font-weight: 500;")
        main_layout.addWidget(lbl_footer)
        
    def validar_formulario(self):
        """Verifica se todos os campos obrigatórios estão preenchidos para habilitar o botão."""
        nome_valido = len(self.txt_nome.text().strip()) >= 3
        idade_valido = len(self.txt_idade.text().strip()) > 0
        
        # Verifica se pelo menos uma categoria foi selecionada
        alguma_categoria = any(btn.isChecked() for btn in self.temas_botoes)
        
        self.btn_jogar.setEnabled(nome_valido and idade_valido and alguma_categoria)
        
    def ao_jogar_clicado(self):
        """Coleta as informações e envia através do sinal de início de jogo."""
        temas_selecionados = []
        if self.btn_esportes.isChecked():
            temas_selecionados.append("Esportes")
        if self.btn_saude.isChecked():
            temas_selecionados.append("Cinema")
        if self.btn_tecnologia.isChecked():
            temas_selecionados.append("Tecnologia")
        if self.btn_ciencia.isChecked():
            temas_selecionados.append("Ciencia")
            
        dados = {
            "nome": self.txt_nome.text().strip(),
            "idade": int(self.txt_idade.text().strip()),
            "temas": temas_selecionados,
            "consentimento": self.chk_consent.isChecked()
        }
        self.iniciar_jogo_signal.emit(dados)
        
    def resetar_formulario(self):
        """Limpa o formulário para uma nova partida."""
        self.txt_nome.clear()
        self.txt_idade.clear()
        self.chk_consent.setChecked(True)
        for btn in self.temas_botoes:
            btn.setChecked(False)
        self.btn_jogar.setEnabled(False)

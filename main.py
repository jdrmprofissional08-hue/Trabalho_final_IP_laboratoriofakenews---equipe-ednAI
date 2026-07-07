# -*- coding: utf-8 -*-

import sys
import random
from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PySide6.QtCore import Qt

from src.styles import STYLE_SHEET
from src.ui.tela_inicial import TelaInicial
from src.ui.tela_quiz import TelaQuiz
from src.ui.tela_feedback import TelaFeedback
from src.ui.tela_final import TelaFinal
from src.ui.tela_ranking import TelaRanking

# Banco de dados de perguntas simuladas (para demonstrar o jogo de forma 100% funcional)
BANCO_PERGUNTAS = [
    {
        "tema": "Tecnologia",
        "manchete": "Cientistas descobrem algoritmo que lê pensamentos humanos com 100% de precisão",
        "texto": "Segundo a publicação, uma equipe internacional de neurocientistas teria criado uma rede neural de leitura de pensamentos sem nenhuma margem de erro, tornando totalmente obsoletos os testes e diagnósticos psicológicos clássicos.",
        "is_fato": False,
        "explicacao": "Esta notícia é FAKE. Embora existam pesquisas científicas de ponta que correlacionam imagens de ressonância magnética com padrões de linguagem, nenhuma tecnologia possui 100% de acerto ou substitui exames tradicionais de psicologia clínica.",
        "fonte": "G1 - Fato ou Fake",
        "tempo": "há 2 horas",
        "fonte_url": "https://g1.globo.com/fato-ou-fake/"
    },
    {
        "tema": "Saude",
        "manchete": "UFCAT promove campanha gratuita de bem-estar e conscientização em saúde mental no campus",
        "texto": "A ação promove rodas de conversa com profissionais da psicologia, oficinas práticas de relaxamento e distribuição de informativos de apoio pedagógico para estudantes em preparação aos exames semestrais.",
        "is_fato": True,
        "explicacao": "Esta notícia é FATO. A Universidade Federal de Catalão realiza ações contínuas voltadas à saúde mental de seus discentes por meio da Pró-Reitoria de Políticas Estudantis (PROEST) e do setor psicopedagógico.",
        "fonte": "Portal UFCAT",
        "tempo": "há 1 dia",
        "fonte_url": "https://www.ufcat.edu.br"
    },
    {
        "tema": "Esportes",
        "manchete": "Novo suplemento sintético importado garante dobrar a massa muscular de atletas em 15 dias sem doping",
        "texto": "A fabricante afirma que a substância 'MyoMax' altera temporariamente a síntese de proteínas a nível mitocondrial rápido, acelerando o metabolismo e escapando 100% de qualquer controle e teste antidoping do comitê internacional.",
        "is_fato": False,
        "explicacao": "Esta notícia é FAKE. Não há compostos seguros ou milagrosos capazes de dobrar o ganho muscular nesse intervalo de tempo. Alegações de '100% livre de doping' com efeitos anabólicos extremos são comumente farsas comerciais de alto risco à saúde.",
        "fonte": "UOL Esporte - Confere",
        "tempo": "há 3 horas",
        "fonte_url": "https://www.uol.com.br"
    },
    {
        "tema": "Ciencia",
        "manchete": "Telescópio James Webb detecta presença estável de vapor de água em exoplaneta de zona habitável",
        "texto": "A agência espacial e astrofísicos confirmaram que a espectroscopia atmosférica do astro rochoso indicou assinaturas nítidas de H2O gasoso, dando passos largos no estudo sobre potencial biológico em outros sistemas solares.",
        "is_fato": True,
        "explicacao": "Esta notícia é FATO. O telescópio espacial James Webb da NASA/ESA tem revolucionado a exploração espacial coletando dados cruciais e analisando o perfil químico e espectral de planetas rochosos extrassolares distantes.",
        "fonte": "NASA Exoplanet Science",
        "tempo": "há 5 horas",
        "fonte_url": "https://exoplanets.nasa.gov/"
    },
    {
        "tema": "Tecnologia",
        "manchete": "Celulares a partir de 2026 recarregarão a bateria apenas captando radiação das ondas Wi-Fi do ambiente",
        "texto": "Engenheiros teriam integrado um microrreceptor flexível que supostamente absorve o sinal de roteadores e carrega aparelhos de 0 a 100% em menos de 10 minutos, sem fios e sem contato direto com a tomada.",
        "is_fato": False,
        "explicacao": "Esta notícia é FAKE. O aproveitamento de energia por ondas eletromagnéticas de redes de comunicação (RF harvesting) atua apenas na escala de micro-watts. Violar os limites de absorção para recarga rápida de smartphones é fisicamente impossível e ilegal.",
        "fonte": "Tecnoblog - Fake Check",
        "tempo": "há 6 horas",
        "fonte_url": "https://tecnoblog.net"
    },
    {
        "tema": "Saude",
        "manchete": "Pesquisa brasileira desenvolve terapia fotodinâmica que trata lesões de pele com redução de 70% no custo",
        "texto": "O projeto é encabeçado por cientistas de universidades federais públicas em parceria com institutos federais, utilizando medicamentos de base fotossensibilizante associados a LEDs em tratamentos alternativos contra lesões dermatológicas.",
        "is_fato": True,
        "explicacao": "Esta notícia é FATO. A pesquisa brasileira é referência mundial em terapias fotodinâmicas aplicadas à saúde humana. Diversas iniciativas públicas e acadêmicas geram tratamentos viáveis e acessíveis com luz contra câncer e infecções.",
        "fonte": "Ministério da Saúde",
        "tempo": "há 12 horas",
        "fonte_url": "https://www.gov.br/saude"
    }
]

class EdnAIApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ednAI - Laboratório de Combate a Fake News")
        self.resize(700, 750)
        self.setMinimumSize(450, 650)
        
        # Variáveis de Controle de Estado da Partida
        self.jogador_nome = ""
        self.jogador_idade = 0
        self.jogador_consentimento = True
        self.questoes_selecionadas = []
        self.pergunta_atual_idx = 0
        self.respostas_corretas = 0
        
        # Histórico do Ranking Geral (Iniciado com dados mockados)
        self.lista_ranking = [
            {"nome": "Júlia Mendes", "pontos": "4/4"},
            {"nome": "Rafael Costa", "pontos": "3/4"},
            {"nome": "Bianca Oliveira", "pontos": "3/4"},
            {"nome": "Lucas Pereira", "pontos": "2/4"},
            {"nome": "Marina Alves", "pontos": "2/4"},
        ]
        
        # Stacked Widget para empilhar e alternar entre as telas
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
        # Instanciação das Telas da Aplicação
        self.tela_inicial = TelaInicial()
        self.tela_quiz = TelaQuiz()
        self.tela_feedback = TelaFeedback()
        self.tela_final = TelaFinal()
        self.tela_ranking = TelaRanking()
        
        # Inserção das Telas no Widget Empilhado
        self.stacked_widget.addWidget(self.tela_inicial)
        self.stacked_widget.addWidget(self.tela_quiz)
        self.stacked_widget.addWidget(self.tela_feedback)
        self.stacked_widget.addWidget(self.tela_final)
        self.stacked_widget.addWidget(self.tela_ranking)
        
        # Conexão de Sinais para Ações de Controle
        self.tela_inicial.iniciar_jogo_signal.connect(self.iniciar_jogo)
        self.tela_quiz.resposta_signal.connect(self.processar_resposta)
        self.tela_feedback.proxima_pergunta_signal.connect(self.seguir_fluxo)
        self.tela_final.jogar_novamente_signal.connect(self.voltar_inicio)
        self.tela_final.ver_ranking_signal.connect(self.mostrar_ranking)
        self.tela_ranking.voltar_inicio_signal.connect(self.voltar_inicio)
        
        # Define a tela inicial como o foco padrão de abertura
        self.stacked_widget.setCurrentWidget(self.tela_inicial)

    def iniciar_jogo(self, dados_jogador):
        """Prepara a partida filtrando as manchetes baseadas nos temas marcados."""
        self.jogador_nome = dados_jogador["nome"]
        self.jogador_idade = dados_jogador["idade"]
        self.jogador_consentimento = dados_jogador["consentimento"]
        temas_escolhidos = dados_jogador["temas"]
        
        # Filtragem de perguntas baseando-se nos checkboxes ativados
        perguntas_filtradas = [q for q in BANCO_PERGUNTAS if q["tema"] in temas_escolhidos]
        
        # Se nenhuma pergunta coincidir por segurança (fallback)
        if not perguntas_filtradas:
            perguntas_filtradas = list(BANCO_PERGUNTAS)
            
        # Sorteia as perguntas filtradas
        random.shuffle(perguntas_filtradas)
        # O jogo terá no máximo 4 rodadas
        self.questoes_selecionadas = perguntas_filtradas[:4]
        
        self.pergunta_atual_idx = 0
        self.respostas_corretas = 0
        
        self.exibir_pergunta_atual()
        self.stacked_widget.setCurrentWidget(self.tela_quiz)
        
    def exibir_pergunta_atual(self):
        """Carrega a questão e atualiza os rótulos de progresso."""
        pergunta = self.questoes_selecionadas[self.pergunta_atual_idx]
        self.tela_quiz.carregar_pergunta(pergunta)
        self.tela_quiz.atualizar_progresso(
            self.pergunta_atual_idx + 1, 
            len(self.questoes_selecionadas)
        )
        
    def processar_resposta(self, resposta_jogador):
        """Compara a escolha do usuário com o gabarito e ativa o feedback educativo."""
        pergunta = self.questoes_selecionadas[self.pergunta_atual_idx]
        acertou = (resposta_jogador == pergunta["is_fato"])
        
        if acertou:
            self.respostas_corretas += 1
            
        eh_ultima = (self.pergunta_atual_idx == len(self.questoes_selecionadas) - 1)
        
        # Transiciona para o feedback
        self.tela_feedback.exibir_feedback(
            acertou=acertou,
            explicacao_texto=pergunta["explicacao"],
            link_texto=f"Verificação completa no {pergunta['fonte']}",
            link_url=pergunta["fonte_url"],
            eh_ultima=eh_ultima
        )
        self.stacked_widget.setCurrentWidget(self.tela_feedback)
        
    def seguir_fluxo(self):
        """Decide se passa para a próxima questão ou encerra a partida."""
        if self.pergunta_atual_idx < len(self.questoes_selecionadas) - 1:
            self.pergunta_atual_idx += 1
            self.exibir_pergunta_atual()
            self.stacked_widget.setCurrentWidget(self.tela_quiz)
        else:
            # Fim do jogo: define os valores finais da tela de pontuação
            self.tela_final.exibir_resultados(
                self.respostas_corretas, 
                len(self.questoes_selecionadas)
            )
            
            # Registra no ranking se houver autorização
            if self.jogador_consentimento:
                # Remove registros de testes antigos do jogador ativo se existirem
                self.lista_ranking = [r for r in self.lista_ranking if f"{self.jogador_nome} (Você)" not in r["nome"]]
                
                registro = {
                    "nome": f"{self.jogador_nome} (Você)", 
                    "pontos": f"{self.respostas_corretas}/{len(self.questoes_selecionadas)}"
                }
                self.lista_ranking.append(registro)
                
                # Reordena a tabela com base na pontuação máxima decrescente
                def obter_acertos(item):
                    try:
                        return int(item["pontos"].split("/")[0])
                    except ValueError:
                        return 0
                self.lista_ranking.sort(key=obter_acertos, reverse=True)
                
            self.stacked_widget.setCurrentWidget(self.tela_final)
            
    def mostrar_ranking(self):
        """Alimenta a tela de classificação e a exibe."""
        self.tela_ranking.definir_dados_ranking(self.lista_ranking)
        self.stacked_widget.setCurrentWidget(self.tela_ranking)
        
    def voltar_inicio(self):
        """Limpa as seleções antigas do formulário e retorna à identificação."""
        self.tela_inicial.resetar_formulario()
        self.stacked_widget.setCurrentWidget(self.tela_inicial)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Aplica a identidade visual global via QSS
    app.setStyleSheet(STYLE_SHEET)
    
    win = EdnAIApp()
    win.show()
    sys.exit(app.exec())

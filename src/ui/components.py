# -*- coding: utf-8 -*-

from PySide6.QtWidgets import QFrame, QGraphicsDropShadowEffect, QWidget, QSizePolicy
from PySide6.QtGui import QColor, QPainter, QPen, QBrush, QPixmap
from PySide6.QtCore import Qt, QSize

def apply_shadow(widget, blur=15, offset=(0, 4), opacity=20):
    """Aplica um efeito de sombra suave ao widget."""
    shadow = QGraphicsDropShadowEffect(widget)
    shadow.setBlurRadius(blur)
    shadow.setOffset(offset[0], offset[1])
    shadow.setColor(QColor(0, 0, 0, opacity))
    widget.setGraphicsEffect(shadow)

class CardFrame(QFrame):
    """Um frame com estilo de cartão com bordas arredondadas e sombra suave."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("CardFrame")
        apply_shadow(self, blur=18, offset=(0, 6), opacity=15)


class ImagePlaceholder(QWidget):
    """Widget que desenha dinamicamente um placeholder de imagem moderno para as notícias."""
    def __init__(self, text="IMAGEM DA POSTAGEM", parent=None):
        super().__init__(parent)
        self.text = text
        self.image_path = ""
        self.setMinimumHeight(260)
        self.setMaximumHeight(320)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = self.rect()
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(QColor("#F8FAFC")))
        painter.drawRoundedRect(rect, 8, 8)

        if self.image_path:
            pixmap = QPixmap(self.image_path)
            if not pixmap.isNull():
                scaled = pixmap.scaled(
                    self.size(),
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
                x = (self.width() - scaled.width()) // 2
                y = (self.height() - scaled.height()) // 2
                painter.drawPixmap(x, y, scaled)
                return
        
        # Fundo do placeholder (cinza claro suave)
        painter.setBrush(QBrush(QColor("#F1F5F9")))
        painter.drawRoundedRect(rect, 8, 8)
        
        # Desenhar borda tracejada fina
        painter.setPen(QPen(QColor("#CBD5E1"), 1, Qt.DashLine))
        painter.setBrush(Qt.NoBrush)
        painter.drawRoundedRect(rect.adjusted(2, 2, -2, -2), 6, 6)
        
        # Desenhar ícone de imagem simples no centro
        cx = rect.center().x()
        cy = rect.center().y() - 15
        
        painter.setPen(QPen(QColor("#94A3B8"), 2))
        # Desenha contorno do retângulo da câmera
        painter.drawRoundedRect(cx - 25, cy - 15, 50, 30, 4, 4)
        # Lente/Círculo
        painter.drawEllipse(cx - 10, cy - 5, 20, 20)
        # Detalhe superior flash
        painter.drawRect(cx - 18, cy - 20, 10, 5)
        
        # Desenhar o texto descritivo
        painter.setPen(QColor("#64748B"))
        font = painter.font()
        font.setPointSize(11)
        font.setBold(True)
        painter.setFont(font)
        painter.drawText(
            rect.adjusted(10, 110, -10, -10),
            Qt.AlignCenter | Qt.AlignTop,
            self.text
        )

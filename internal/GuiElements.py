from PyQt5.QtWidgets import QPushButton, QGroupBox, QVBoxLayout, QLineEdit

from CurrencyConverter.internal import AppConfigurations as conf


class RightArrowButton(QPushButton):

    def __init__(self):
        super().__init__()
        self.setFixedHeight(conf.CONVERSIONBUTTONHEIGHT)
        self.setFixedWidth(conf.CONVERSIONBUTTONWIDTH)
        self.setText("->")


class LeftArrowButton(QPushButton):

    def __init__(self):
        super().__init__()
        self.setFixedHeight(conf.CONVERSIONBUTTONHEIGHT)
        self.setFixedWidth(conf.CONVERSIONBUTTONWIDTH)
        self.setText("<-")

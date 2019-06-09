from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout,  QGridLayout, QGroupBox
from PyQt5.QtWidgets import QLabel, QPushButton, QLineEdit

from datetime import datetime

import CurrencyConverter.internal.AppConfigurations as conf
from CurrencyConverter.internal.ConversionRateFetcher import ConversionRateFetcher
from CurrencyConverter.internal.Elements import RightArrowButton, LeftArrowButton

import threading

class CurrencyConverterApp(QMainWindow):

    def __init__(self):
        super().__init__()
        self.leftOffSet = conf.LEFTOFFSET
        self.topOffset = conf.TOPOFFSET
        self.width = conf.WIDTH
        self.height = conf.HEIGHT
        # variables
        self.euroMyrConversionRate = 0.00
        self.euroSgdConversionRate = 0.00
        self.statusLabel = QLabel("")
        self.initializeGui()



    def initializeGui(self):
        self.setWindowTitle(f"{conf.TITLE} v{conf.VERSION}")
        mainWindow = QWidget()
        mainLayout = QVBoxLayout()

        # top window the Banner containing the conversion rates
        banner = self.createBanner()
        content = self.createContent()

        mainLayout.addWidget(banner)
        mainLayout.addWidget(content)
        mainWindow.setLayout(mainLayout)

        self.setGeometry(self.leftOffSet, self.topOffset, self.width, self.height)
        self.setCentralWidget(mainWindow)
        self.setWindowTitle(f"{conf.TITLE} v{conf.VERSION}")
        # execute startUpMethods
        self.executeStartUpMethods()
        self.show()

    def createBanner(self) -> QWidget:
        """
        create the banner of the application, containing
        the converion rates and the dates they are checked
        """
        topWindow = QWidget()
        topWindowLayout = QGridLayout()

        self.myrConversionRateLabel = QLabel(f"1 EUR = {self.euroMyrConversionRate:3.4f} MYR")
        self.myrConversionRateDateLabel = QLabel(f"...")
        topWindowLayout.addWidget(self.myrConversionRateLabel, 1, 1, 1, 1)
        topWindowLayout.addWidget(self.myrConversionRateDateLabel, 1, 2, 1, 1)

        self.sgdConversionRateLabel = QLabel(f"1 EUR = {self.euroSgdConversionRate:3.4f} SGD")
        self.sgdConversionRateDateLabel = QLabel(f"...")
        topWindowLayout.addWidget(self.sgdConversionRateLabel, 2, 1, 1, 1)
        topWindowLayout.addWidget(self.sgdConversionRateDateLabel, 2, 2, 1, 1)

        self.refreshButton = QPushButton()
        self.refreshButton.setFixedHeight(40)
        self.refreshButton.setFixedWidth(40)
        self.refreshButton.setText("*")
        self.refreshButton.clicked.connect(self.refreshRates)
        topWindowLayout.addWidget(self.refreshButton, 1, 3, 2, 1)

        topWindow.setLayout(topWindowLayout)
        topWindow.setStyleSheet("background-color: white")
        topWindow.setAutoFillBackground(True)
        topWindow.setFixedHeight(conf.BANNERHEIGHT)
        topWindow.setFixedWidth(conf.BANNERWIDTH)
        return topWindow

    def createContent(self) -> QWidget:
        """
        create the content part of the conversion application
        """
        content = QWidget()
        contentLayout = QGridLayout()

        euroBox = QGroupBox("EUR")
        euroBoxLayout = QVBoxLayout()
        self.euroValue = QLineEdit()
        self.euroValue.setFixedHeight(conf.INPUTFIELDHEIGHT)
        euroBoxLayout.addWidget(self.euroValue)
        euroBox.setLayout(euroBoxLayout)
        contentLayout.addWidget(euroBox, 1, 1, 3, 1)

        self.toMyrButton = RightArrowButton()
        self.toMyrButton.clicked.connect(self.convertEURtoMYR)
        contentLayout.addWidget(self.toMyrButton, 2, 2, 1, 1)
        self.fromMyrButton = LeftArrowButton()
        self.fromMyrButton.clicked.connect(self.convertMYRtoEUR)
        contentLayout.addWidget(self.fromMyrButton, 3, 2, 1, 1)

        myrBox = QGroupBox("MYR")
        myrBoxLayout = QVBoxLayout()
        self.myrValue = QLineEdit()
        self.myrValue.setFixedHeight(conf.INPUTFIELDHEIGHT)
        myrBoxLayout.addWidget(self.myrValue)
        myrBox.setLayout(myrBoxLayout)
        contentLayout.addWidget(myrBox, 1, 3, 3, 1)

        self.toSgdButton = RightArrowButton()
        self.toSgdButton.clicked.connect(self.convertEURtoSGD)
        contentLayout.addWidget(self.toSgdButton, 5, 2, 1, 1)
        self.fromSgdButton = LeftArrowButton()
        self.fromSgdButton.clicked.connect(self.convertSGDtoEUR)
        contentLayout.addWidget(self.fromSgdButton, 6, 2, 1, 1)

        sgdBox = QGroupBox("SGD")
        sgdBoxLayout = QVBoxLayout()
        self.sgdValue = QLineEdit()
        self.sgdValue.setFixedHeight(conf.INPUTFIELDHEIGHT)
        sgdBoxLayout.addWidget(self.sgdValue)
        sgdBox.setLayout(sgdBoxLayout)
        contentLayout.addWidget(sgdBox, 4, 3, 3, 1)

        # status information
        contentLayout.addWidget(QLabel("Status:"), 5, 1, 1, 1)
        contentLayout.addWidget(self.statusLabel, 6, 1, 1, 1)

        content.setLayout(contentLayout)
        content.setFixedWidth(conf.CONTENTWIDTH)
        content.setFixedHeight(conf.CONTENTHEIGHT)
        return content

    def convertEURtoMYR(self):
        """
        convert from EUR to MYR
        """
        euroInput = self.getEuroInput()
        myrValue = euroInput * self.euroMyrConversionRate
        self.myrValue.setText(f"{myrValue:4.2f}")

    def convertMYRtoEUR(self):
        """
        convert from MYR to EUR
        """
        myrInput = self.getMYRInput()
        euroValue = myrInput / self.euroMyrConversionRate
        self.euroValue.setText(f"{euroValue:4.2f}")

    def convertEURtoSGD(self):
        """
        convert from EUR to SGD
        """
        euroInput = self.getEuroInput()
        sgdValue = euroInput * self.euroSgdConversionRate
        self.sgdValue.setText(f"{sgdValue:4.2f}")

    def convertSGDtoEUR(self):
        """
        convert from SGD to EUR
        """
        sgdInput = self.getSgdInput()
        euroValue = sgdInput / self.euroSgdConversionRate
        self.euroValue.setText(f"{euroValue:4.2f}")

    def executeStartUpMethods(self):
        self.statusLabel.setText("Initially obtaining conversion rates...")
        initUpdateThread = threading.Thread(target=self.updateConversionRate, args=("StartupConversionThread", ))
        initUpdateThread.start()

    def refreshRates(self):
        self.statusLabel.setText("Refreshing conversion rates...")
        refreshThread = threading.Thread(target=self.updateConversionRate, args=("RefreshConversionRate", ))
        refreshThread.start()

    def getEuroInput(self):
        try:
            return float(self.euroValue.text())
        except:
            return None

    def getMYRInput(self):
        try:
            return float(self.myrValue.text())
        except:
            return None

    def getSgdInput(self):
        try:
            return float(self.sgdValue.text())
        except:
            return None


    def updateConversionRate(self, threadname="ConversionRateUpdateThread"):
        print(f"[{threadname}] Fetching current conversion rate and updating it")
        convMYRfetcher = ConversionRateFetcher()
        convMYRfetcher.fetch()
        myrRateDate = datetime.now()
        convSGDfetcher = ConversionRateFetcher(webpage="https://thecurrencycalculator.com/EUR/SGD/")
        convSGDfetcher.fetch()
        sgdRateDate = datetime.now()
        if convMYRfetcher.fetched:
            # set the values
            print(f"1 Euro = {convMYRfetcher.euroToForeign} MYR")
            self.myrConversionRateLabel.setText(f"1 EUR = {convMYRfetcher.euroToForeign:2.4f} MYR")
            self.myrConversionRateDateLabel.setText(myrRateDate.isoformat(timespec='minutes'))
            self.euroMyrConversionRate = convMYRfetcher.euroToForeign
        if convSGDfetcher.fetched:
            print(f"1 Euro = {convSGDfetcher.euroToForeign} SGD")
            self.sgdConversionRateLabel.setText(f"1 EUR = {convSGDfetcher.euroToForeign:2.4f} SGD")
            self.sgdConversionRateDateLabel.setText(sgdRateDate.isoformat(timespec='minutes'))
            self.euroSgdConversionRate = convSGDfetcher.euroToForeign
        # updating the status line
        self.statusLabel.setText("OK.")

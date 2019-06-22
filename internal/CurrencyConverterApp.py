from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout,  QGridLayout, QGroupBox
from PyQt5.QtWidgets import QLabel, QPushButton, QLineEdit

from datetime import datetime
import unicodedata

import CurrencyConverter.internal.AppConfigurations as conf
from CurrencyConverter.internal.ConversionRateFetcher import ConversionRateFetcher
from CurrencyConverter.internal.History import CurrencyInformation, ConversionHistoryHandler
from CurrencyConverter.internal.GuiElements import RightArrowButton, LeftArrowButton

import threading

class CurrencyConverterApp(QMainWindow):

    def __init__(self, logger):
        super().__init__()
        self.logger = logger    # use the logger to log stuff
        self.leftOffSet = conf.LEFTOFFSET
        self.topOffset = conf.TOPOFFSET
        self.width = conf.WIDTH
        self.height = conf.HEIGHT
        # variables
        self.historyHandler = ConversionHistoryHandler(self.logger)
        self.myrCurrency = CurrencyInformation("MYR")
        self.sgdCurrency = CurrencyInformation("SGD")
        #self.euroMyrConversionRate = 0.00
        #self.euroSgdConversionRate = 0.00
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

        self.myrConversionRateLabel = QLabel(f"1 {unicodedata.lookup('EURO SIGN')} = {self.myrCurrency.rate:3.4f} MYR")
        self.myrConversionRateDateLabel = QLabel(f"...")
        topWindowLayout.addWidget(self.myrConversionRateLabel, 1, 1, 1, 1)
        topWindowLayout.addWidget(self.myrConversionRateDateLabel, 1, 2, 1, 1)

        self.sgdConversionRateLabel = QLabel(f"1 {unicodedata.lookup('EURO SIGN')} = {self.sgdCurrency.rate:3.4f} SGD")
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

        euroBox = QGroupBox(f"EUR {unicodedata.lookup('EURO SIGN')}")
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
        statusBox = QGroupBox("Status")
        statusBoxayout = QVBoxLayout()
        self.statusLabel.setFixedHeight(40)
        statusBoxayout.addWidget(self.statusLabel)

        self.saveHistoryButton = QPushButton()
        self.saveHistoryButton.setText("save history")
        self.saveHistoryButton.clicked.connect(self.historyHandler.saveHistory)
        statusBoxayout.addWidget(self.saveHistoryButton)

        self.showHistoryButton = QPushButton()
        self.showHistoryButton.setText("show history")
        self.showHistoryButton.clicked.connect(self.historyHandler.showHistory)
        statusBoxayout.addWidget(self.showHistoryButton)
        statusBox.setLayout(statusBoxayout)
        #statusBox.setStyleSheet("background-color: white")
        #statusBox.setAutoFillBackground(True)

        contentLayout.addWidget(statusBox, 4, 1, 3, 1)
        content.setLayout(contentLayout)
        content.setFixedWidth(conf.CONTENTWIDTH)
        content.setFixedHeight(conf.CONTENTHEIGHT)
        return content

    def convertEURtoMYR(self):
        """
        convert from EUR to MYR
        """
        euroInput = self.getEuroInput()
        myrValue = euroInput * self.myrCurrency.rate
        self.myrValue.setText(f"{myrValue:4.2f}")

    def convertMYRtoEUR(self):
        """
        convert from MYR to EUR
        """
        myrInput = self.getMYRInput()
        euroValue = myrInput / self.myrCurrency.rate
        self.euroValue.setText(f"{euroValue:4.2f}")

    def convertEURtoSGD(self):
        """
        convert from EUR to SGD
        """
        euroInput = self.getEuroInput()
        sgdValue = euroInput * self.sgdCurrency.rate
        self.sgdValue.setText(f"{sgdValue:4.2f}")

    def convertSGDtoEUR(self):
        """
        convert from SGD to EUR
        """
        sgdInput = self.getSgdInput()
        euroValue = sgdInput / self.sgdCurrency.rate
        self.euroValue.setText(f"{euroValue:4.2f}")

    def executeStartUpMethods(self):
        self.logger.info("Initially obtaining conversion rates ...")
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
            try:
                return float(self.euroValue.text().replace(',', '.'))
            except:
                return None

    def getMYRInput(self):
        try:
            return float(self.myrValue.text())
        except:
            try:
                return float(self.myrValue.text().replace(',', '.'))
            except:
                return None

    def getSgdInput(self):
        try:
            return float(self.sgdValue.text())
        except:
            try:
                return float(self.sgdValue.text().replace(',', '.'))
            except:
                return None

    def updateConversionRate(self, threadname="ConversionRateUpdateThread"):
        self.logger.info(f"[{threadname}] Fetching current conversion rate and updating it")
        convMYRfetcher = ConversionRateFetcher(self.logger)
        convMYRfetcher.fetch()
        myrRateDate = datetime.now()
        convSGDfetcher = ConversionRateFetcher(self.logger, webpage="https://thecurrencycalculator.com/EUR/SGD/")
        convSGDfetcher.fetch()
        sgdRateDate = datetime.now()
        if convMYRfetcher.fetched:
            # set the values
            self.logger.info(f"1 Euro = {convMYRfetcher.euroToForeign} MYR")
            self.myrConversionRateLabel.setText(f"1 {unicodedata.lookup('EURO SIGN')} = {convMYRfetcher.euroToForeign:2.4f} MYR")
            self.myrConversionRateDateLabel.setText(myrRateDate.isoformat(timespec='minutes'))
            self.myrCurrency.rate = convMYRfetcher.euroToForeign
            self.myrCurrency.date = myrRateDate
        if convSGDfetcher.fetched:
            self.logger.info(f"1 Euro = {convSGDfetcher.euroToForeign} SGD")
            self.sgdConversionRateLabel.setText(f"1 {unicodedata.lookup('EURO SIGN')} = {convSGDfetcher.euroToForeign:2.4f} SGD")
            self.sgdConversionRateDateLabel.setText(sgdRateDate.isoformat(timespec='minutes'))
            self.sgdCurrency.rate = convSGDfetcher.euroToForeign
            self.sgdCurrency.date = sgdRateDate
        # updating the status line
        self.statusLabel.setText("OK.")
        if self.historyHandler.isReady:
            self.historyHandler.addCurrencyInformation(self.myrCurrency, self.sgdCurrency)


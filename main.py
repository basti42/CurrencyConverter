from PyQt5.QtWidgets import QApplication
from CurrencyConverter.internal.CurrencyConverterApp import CurrencyConverterApp


if __name__ == "__main__":

    app = QApplication([])

    currencyConverterApp = CurrencyConverterApp()

    app.exec_()

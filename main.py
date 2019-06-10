from PyQt5.QtWidgets import QApplication
from CurrencyConverter.internal.CurrencyConverterApp import CurrencyConverterApp

import logging


if __name__ == "__main__":

    # initializing a proper logger
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # create a file handler
    handler = logging.FileHandler('CurrencyConverter.log')
    handler.setLevel(logging.INFO)

    # create a logging format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(handler)

    # start the main application
    app = QApplication([])
    currencyConverterApp = CurrencyConverterApp(logger)
    app.exec_()

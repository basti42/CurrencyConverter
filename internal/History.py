import numpy as np
import os
import pandas as pd
import dateutil.parser

class CurrencyInformation:
    def __init__(self, currency):
        self.currency = currency
        self.rate = 0.00
        self.date = None


class ConversionHistoryHandler:

    def __init__(self, logger):
        self.logger = logger
        self.filename = os.path.join(os.path.dirname("."), "conversionhistory.csv")
        self.myrHistory = []
        self.sgdHistory = []
        self.isReady = False    # flag required due to multithreading
        self.initialize()

    def initialize(self):
        self.logger.info(f"History file: '{os.path.abspath(self.filename)}'")
        if os.path.exists(self.filename):
            self.logger.info("Initially reading history")
            dataframe = pd.read_csv(self.filename)
            for i, row in dataframe.iterrows():
                currentMyr = CurrencyInformation("MYR")
                currentMyr.rate = float(row[1])
                currentMyr.date = dateutil.parser.parse(row[0])
                self.myrHistory.append(currentMyr)

                currentSgd = CurrencyInformation("SGD")
                currentSgd.rate = float(row[3])
                currentSgd.date = dateutil.parser.parse(row[2])
                self.sgdHistory.append(currentSgd)
        else:
            self.logger.info("No history file found")
        self.isReady = True

    def addCurrencyInformation(self, myr, sgd):
        """
        append new currency information to the history lists
        """
        self.myrHistory.append(myr)
        self.sgdHistory.append(sgd)
        self.logger.info("Added new currency information to history")

    def saveHistory(self):
        tmpdict = dict()
        tmpdict['myr_dates'] = [c.date for c in self.myrHistory]
        tmpdict['myr_rates'] = [c.rate for c in self.myrHistory]
        tmpdict['sgd_dates'] = [c.date for c in self.sgdHistory]
        tmpdict['sgd_rates'] = [c.rate for c in self.sgdHistory]
        self.logger.info("Writing history to file")
        outframe = pd.DataFrame(tmpdict)
        outframe.to_csv(self.filename, index=False)

    def showHistory(self):
        pass
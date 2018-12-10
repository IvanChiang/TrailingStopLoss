import pandas as pd
from pathlib import Path
import logging

log = logging.getLogger(__name__)


class TrailingStopLoss:
    COLUMN = [str(i) for i in range(20)] + ['current_price', 'stop_percent', 'trailing_price', 'enabled']
    FILE_NAME = r"TSLManager.csv"

    def __init__(self, order, curr, percent, evt):
        posFile = Path(self.FILE_NAME)
        if posFile.exists():
            log.debug("position file exist! load from it!")
            self.__data = pd.read_csv(posFile)
        else:
            log.debug("position file not exist! new an empty data!")
            self.__data = pd.DataFrame(columns=self.COLUMN)
        # self.__orderno = order
        # self.__currPrice = curr
        # self.__stopPercent = percent
        # self.__stopPrice = self.__currPrice - self.__currPrice * self.__stopPercent
        # self.__stopLostEvt = evt

    def add(self, monitor_target):
        monitor_target_l = monitor_target.split(',')
        stock_id = monitor_target_l[3]
        if stock_id not in self.__data.index and self.__data.at[stock_id, 'enabled'] == 1:
            self.__data.loc[stock_id] = monitor_target_l
            self.__data.loc[stock_id, 'enabled'] = 1
            curr_price = self.__data.at[stock_id, 'current_price'] = monitor_target_l[4]
            stop_percent = self.__data.at[stock_id, 'stop_percent'] = 0.1
            self.__data.at[stock_id, 'trailing_price'] = curr_price - curr_price * stop_percent

    def update(self, stock_id, curr_price):
        self.__data.loc[stock_id, 'current_price'] = curr_price

        stop_percent = self.__data.loc[stock_id, 'stop_percent']
        trailing_price = self.__data.loc[stock_id, 'trailing_price']
        if curr_price - curr_price * stop_percent > trailing_price:
            self.__data.loc[stock_id, 'trailing_price'] = curr_price - curr_price * stop_percent

        if curr_price < trailing_price:
            self.__stopLostEvt()
            # self.remove()

            self.__data.loc[stock_id, 'enabled'] = 0

        # sync to file
        self.__data.to_csv(self.FILE_NAME)

    def remove(self):
        del self

    def __del__(self):
        logging.info('delete trailing stop order')

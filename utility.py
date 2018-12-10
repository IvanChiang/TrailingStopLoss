import logging
from pathlib import Path

import pandas as pd
from pushbullet import Pushbullet

log = logging.getLogger(__name__)


class PositionMgn:
    COLUMN = [str(i) for i in range(22)] + ['current_price', 'stop_percent', 'trailing_price', 'enabled']
    FILE_NAME = r"TSLManager.csv"

    def __init__(self):

        self.pb = Pushbullet(r'o.rLhRu7uqYBERqfd473GTZcRKOQY1Ok0V')

        posFile = Path(self.FILE_NAME)
        if posFile.exists():
            log.debug("position file exist! load from it!")
            self.__data = pd.read_csv(posFile, index_col=0)
            log.debug("\n%s", self.__data)
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
        stock_id = monitor_target_l[2]
        if stock_id not in self.__data.index:
            curr_price = float(monitor_target_l[5])
            stop_percent = 0.1
            self.__data.loc[stock_id] = monitor_target_l + [curr_price, stop_percent,
                                                            (curr_price - curr_price * stop_percent), 1]

        log.debug("\n%s", self.__data)

        self.sync()

    def getSubscribeList(self):
        return self.__data.index

    def sync(self):
        # sync to file
        self.__data.to_csv(self.FILE_NAME)

    def update(self, stock_id, curr_price):
        log.debug('update: %s, %f', stock_id, curr_price)
        self.__data.loc[stock_id, 'current_price'] = curr_price

        stop_percent = self.__data.loc[stock_id, 'stop_percent']
        trailing_price = self.__data.loc[stock_id, 'trailing_price']
        if curr_price - curr_price * stop_percent > trailing_price:
            self.__data.loc[stock_id, 'trailing_price'] = curr_price - curr_price * stop_percent

        if curr_price < trailing_price:
            self.pb.push_note(stock_id, "stop loss now!")

            self.__data.loc[stock_id, 'enabled'] = 0

        self.sync()

    def remove(self):
        del self

    def __del__(self):
        logging.info('delete trailing stop order')

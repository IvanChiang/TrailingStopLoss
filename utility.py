import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s : %(message)s',
                    datefmt='%Y%m%dT%H%M%S')
logging.info('Info message')


class TrailingStopLoss:

    def __init__(self, order, curr, percent, evt):
        self.__orderno = order
        self.__currPrice = curr
        self.__stopPercent = percent
        self.__stopPrice = self.__currPrice - self.__currPrice*self.__stopPercent
        self.__stopLostEvt = evt

    def update(self, curr_price):
        self.__currPrice = curr_price

        if self.__currPrice - self.__currPrice * self.__stopPercent > self.__stopPrice:
            self.__stopPrice = self.__currPrice - self.__currPrice * self.__stopPercent

        if self.__currPrice < self.__stopPrice:
            self.__stopLostEvt()
            self.remove()

    def remove(self):
        del self

    def __del__(self):
        logging.info('delete trailing stop order')

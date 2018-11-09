from utility import TrailingStopLoss
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s : %(message)s',
                    datefmt='%Y%m%dT%H%M%S')
logging.info('Info message')

if __name__ == '__main__':
    def callback():
        logging.info('stop loss')


    s = TrailingStopLoss('xxxxx', 30, 0.1, callback)



    for i in range(5):
        s.update(i)

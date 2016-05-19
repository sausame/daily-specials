import sys

from model import WareManager

if __name__ == '__main__':

    reload(sys)
    sys.setdefaultencoding('utf8')

    manager = WareManager(True)
    manager.initWareList()
    manager.updatePriceHistories()
    manager.outputHtml()


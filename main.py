import sys

from model import WareManager

if __name__ == '__main__':

    reload(sys)
    sys.setdefaultencoding('utf8')

    isLocal = True

    if len(sys.argv) > 1 and 'false' == sys.argv[1].lower():
        isLocal = False

    manager = WareManager(isLocal)
    manager.initWareList()
    manager.updatePriceHistories()
    manager.outputHtml()
    manager.outputMarkdown()


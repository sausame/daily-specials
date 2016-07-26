import sys

from model import WareManager

if __name__ == '__main__':

    reload(sys)
    sys.setdefaultencoding('utf8')

    isLocal = True
    configPath = None

    if len(sys.argv) > 1 and 'false' == sys.argv[1].lower():
        isLocal = False

    if len(sys.argv) > 2:
        configPath = sys.argv[2]

    manager = WareManager(isLocal)
    manager.initWareList()
    manager.updatePriceHistories()
    manager.outputMarkdown()
    manager.outputHtml()

    if configPath:
        manager.uploadHtmlToFtp(configPath)


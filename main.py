import os, sys, time

from datetime import datetime
from model import WareManager

if __name__ == '__main__':

    reload(sys)
    sys.setdefaultencoding('utf8')

    os.environ['TZ'] = 'Asia/Shanghai'
    time.tzset()

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
    manager.outputJson()
    manager.outputHtml()

    if configPath:
        manager.uploadHtmlToFtp(configPath)


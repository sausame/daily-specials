import os, random, sys, time

from datetime import datetime
from ftp import uploadFtp
from history import HhHistoryParser
from js import JsExecutor
from network import saveHttpData
from utils import getProperty, removeOverdueFiles
from source import SeckillInfo
from ware import WareItem, WareDisplayer

class WareManager:

    def __init__(self, isLocal=False):
        self.isLocal = isLocal
        self.wareList = []

        try:
            os.mkdir('data')
        except OSError:
            pass

    def initWareList(self):

        if not self.isLocal:
            # Remove overdue files
            removeOverdueFiles('data/', 47 * 3600, '.js') # Almost two days overdue
            removeOverdueFiles('data/', 11 * 3600, '.json') # Almost half of one day overdue

        # Update from Jd
        self.updateJdWareList()

    def getJdGids(self):

        gids = []
        gid = 26

        path = 'data/%d.json' % gid

        print "Retrieve {} for indexes".format(path)

        if not self.isLocal:
            ret = saveHttpData(path, 'http://coupon.m.jd.com/seckill/seckillList.json?gid=%d' % gid)
            if ret < 0: return gids

        seckillInfo = SeckillInfo(path)

        # Find all matchesItems
        for matchesItem in seckillInfo.matchesList:
            gids += matchesItem.gid,

        return gids

    def updateJdWareList(self):

        gids = self.getJdGids()

        for gid in gids:
            path = 'data/%d.json' % gid

            if not self.isLocal:

                cached = os.path.exists(path)
                if not cached:

                    print "Retrieve {}".format(path)

                    ret = saveHttpData(path, 'http://coupon.m.jd.com/seckill/seckillList.json?gid=%d' % gid)
                    if ret < 0: continue

            seckillInfo = SeckillInfo(path)

            # Find current matchesItem
            for matchesItem in seckillInfo.matchesList:

                if matchesItem.gid == gid:
                    break;

            # Set ware items
            for item in seckillInfo.itemList:

                wItem = WareItem()
                wItem.setSeckillItem(item, matchesItem)

                self.wareList.append(wItem)

            # os.remove(path)

            # Sleep for a while
            if not self.isLocal and not cached:
                time.sleep(random.random())

    def updatePriceHistories(self):

        def execute(executor, title, url):
            return executor.context.requestPriceInfo(title, url)

        executor = JsExecutor('js/huihui.js')

        for ware in self.wareList:

            # Get URL for price history
            url = execute(executor, ware.name, ware.baseUrl)

            # Get price histories
            path = 'data/{}.js'.format(ware.wid)

            # Update from servers
            if not self.isLocal:

                cached = os.path.exists(path)
                if not cached:

                    print 'Update {}'.format(ware.wid)
                    ret = saveHttpData(path, url)
                    if ret < 0: continue

            # Parse
            parser = HhHistoryParser()

            if parser.parse(path):
                historyData = parser.getHistoryData()
                if historyData:
                    ware.setHistories(historyData.histories)

            ware.update()

            # os.remove(path)

            # Sleep for a while
            if not self.isLocal and not cached:
                time.sleep(random.random())

        self.wareList.sort()

    def outputJson(self):

        path = 'data/index.json'
        fpOut = open(path, 'w')

        with open('json/header.json') as fp:
            fpOut.write(fp.read())

        count = 0

        for ware in self.wareList:

            displayer = WareDisplayer()

            data = displayer.outputJson(ware)
            if data:
                if 0 != count:
                    data = ',' + data

                fpOut.write(data)
                count += 1

        with open('json/footer.json') as fp:

            template = fp.read()
            today = datetime.now().strftime('%Y-%m-%d')

            fpOut.write(template.format(today, count) + '}')

        fpOut.close()

        print '"{}" of "{}" items are outputed to "{}".'.format(count, len(self.wareList), path)

    def outputHtml(self):

        today = datetime.now().strftime('%Y-%m-%d')

        path = 'data/index.html'
        fpOut = open(path, 'w')

        with open('html/header.html') as fp:

            template = fp.read()
            fpOut.write(template.format(today))

        count = 0

        for ware in self.wareList:

            displayer = WareDisplayer()

            data = displayer.outputHtml(ware)

            if data:
                fpOut.write(data)

                if count >= 10: # The first 10 items
                    break

                count += 1

        with open('html/footer.html') as fp:

            fpOut.write(fp.read())

        fpOut.close()

        print '"{}" of "{}" items are outputed to "{}".'.format(count, len(self.wareList), path)

    def outputMarkdown(self):

        today = datetime.now().strftime('%Y-%m-%d')

        path = 'data/index.md'
        fpOut = open(path, 'w')

        with open('markdown/header.md') as fp:

            template = fp.read()
            fpOut.write(template.format(today))

        count = 0;

        for ware in self.wareList:

            displayer = WareDisplayer()

            data = displayer.outputMarkdown(ware, count)
            if data:
                count += 1;
                fpOut.write(data)

        fpOut.close()

        print '"{}" of "{}" items are outputed to "{}".'.format(count, len(self.wareList), path)

    def uploadHtmlToFtp(self, path):

        host = getProperty(path, 'host')
        user = getProperty(path, 'user')
        passwd = getProperty(path, 'passwd')
        dirname = getProperty(path, 'dirname')

        flag = getProperty(path, 'isProtected')
        if flag and 'true' == flag.lower():
            isProtected = True
        else:
            isProtected = False

        uploadFtp(host, dirname, 'data/index.html', user, passwd, isProtected)
        uploadFtp(host, '{}/json'.format(dirname), 'data/index.json', user, passwd, isProtected)


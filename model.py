import os, random, sys, time

from datetime import datetime
from ware import WareItem, WareDisplayer
from js import JsExecutor
from source import SeckillInfo
from history import HhHistoryParser
from network import saveHttpData

class WareManager:

    def __init__(self, isLocal=False):
        self.isLocal = isLocal
        self.wareList = []

        try:
            os.mkdir('data')
        except OSError:
            pass

    def initWareList(self):

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

            print "Retrieve {}".format(path)

            if not self.isLocal:
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
            if not self.isLocal:
                time.sleep(random.random())

    def updatePriceHistories(self):

        def execute(executor, title, url):
            value = 'requestPriceInfo("{}", "{}")'.format(title, url)

            return executor.execute(value)

        executor = JsExecutor('js/huihui.js')

        for ware in self.wareList:

            # Get URL for price history
            url = execute(executor, ware.name, ware.baseUrl)

            # Get price histories
            path = 'data/{}.js'.format(ware.wid)

            # Update from servers
            if not self.isLocal:
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
            if not self.isLocal:
                time.sleep(random.random())

        self.wareList.sort()

    def outputHtml(self):

        today = datetime.now().strftime('%Y-%m-%d')

        path = 'data/index.html'
        fpOut = open(path, 'w')

        with open('html/header.html') as fp:

            template = fp.read()
            fpOut.write(template.format(today))

        for ware in self.wareList:

            displayer = WareDisplayer()

            data = displayer.outputHtml(ware)
            if data:
                fpOut.write(data)

        with open('html/footer.html') as fp:

            fpOut.write(fp.read())

        fpOut.close()

        print '"{}" items are outputed to "{}".'.format(len(self.wareList), path)

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


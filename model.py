import os, random, sys, time

from ware import WareItem
from js import JsExecutor
from source import SeckillInfo
from history import HhHistoryParser
from network import saveHttpData

class WareManager:

    def __init__(self):
        self.wareList = []

        try:
            os.mkdir('data')
        except OSError:
            pass

    def initWareList(self):

        # Update from Jd
        self.updateJdWareList()

    def updateJdWareList(self):

        start = 26
        size = 5
        gids = [x for x in range(start, start + size)]

        for gid in gids:
            path = 'data/%d.json' % gid

            ret = saveHttpData(path, 'http://coupon.m.jd.com/seckill/seckillList.json?gid=%d' % gid)

            if ret < 0: continue

            seckillInfo = SeckillInfo(path)

            for item in seckillInfo.itemList:

                wItem = WareItem()
                wItem.setSeckillItem(item)

                self.wareList.append(wItem)

            # os.remove(path)

    def updatePriceHistories(self):

        def execute(executor, title, url):
            value = 'requestPriceInfo("{}", "{}")'.format(title, url)

            return executor.execute(value)

        executor = JsExecutor('js/huihui.js')

        for ware in self.wareList:

            # Get URL for price history
            url = execute(executor, ware.name, ware.url);

            # Get price histories
            path = 'data/{}.js'.format(ware.wid)
            ret = saveHttpData(path, url)

            # Parse
            parser = HhHistoryParser()

            print ware.wid

            if parser.parse(path):
                historyData = parser.getHistoryData()
                ware.setHistories(historyData.histories)

            # os.remove(path)

            print ware

            # Sleep for a while
            time.sleep(random.random())


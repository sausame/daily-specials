from datetime import tzinfo, timedelta, datetime

class PriceHistory:

    def __init__(self, **kwargs):
        self.set(**kwargs)

    def set(self, **kwargs):
        for keyword in ["price", "time"]:
            setattr(self, keyword, kwargs[keyword])

    def __repr__(self):
        fields = ['    {}={!r}'.format(k, v)
            for k, v in self.__dict__.items() if not k.startswith("_")]

        return "  {}:\n{}".format(self.__class__.__name__, '\n'.join(fields))

class WareItem:

    def __init__(self):
        self.histories = []

    def setSeckillItem(self, item):

        # Basic
        self.wid = item.wareId
        self.name = item.wname

        # Prices
        self.price = item.miaoShaPrice
        self.histories.append(PriceHistory(price=item.jdPrice, time=datetime.now().strftime("%Y-%m-%d")))

        # Start and end times
        self.startTime = item.startTimeShow
        self.endTime = (item.endRemainTime - item.startRemainTime) / 3600

        # URL
        self.url = 'http://item.m.jd.com/product/%s.html' % item.wareId
        self.imageurl = item.imageurl

    def setHistories(self, histories):

        # Histories
        self.histories += histories

    def __repr__(self):
        fields = ['    {}={}'.format(k, v)
            for k, v in self.__dict__.items() if not k.startswith("_") and 'histories' != k]

        str = ''
        for history in self.histories:
            str += '{}\n'.format(history)

        return "{}:\n{}\n{}".format(self.__class__.__name__, '\n'.join(fields), str)


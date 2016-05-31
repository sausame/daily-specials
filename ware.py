from datetime import tzinfo, timedelta, datetime
from functools import total_ordering
from operator import attrgetter

class PriceHistory:

    def __init__(self, **kwargs):
        self.set(**kwargs)

    def set(self, **kwargs):
        for keyword in ['price', 'time']:
            setattr(self, keyword, kwargs[keyword])

    def __repr__(self):
        fields = ['    {}={!r}'.format(k, v)
            for k, v in self.__dict__.items() if not k.startswith('_')]

        return '  {}:\n{}'.format(self.__class__.__name__, '\n'.join(fields))

class Discount:

    def __init__(self):
        pass

    def __repr__(self):
        fields = ['    {}={!r}'.format(k, v)
            for k, v in self.__dict__.items() if not k.startswith('_')]

        return '  {}:\n{}'.format(self.__class__.__name__, '\n'.join(fields))

class Price:

    def __init__(self, price, days, ratio):
        self.price = price
        self.days = days
        self.ratio = ratio

    def __repr__(self):
        fields = ['    {}={!r}'.format(k, v)
            for k, v in self.__dict__.items() if not k.startswith('_')]

        return '  {}:\n{}'.format(self.__class__.__name__, '\n'.join(fields))

@total_ordering
class WareItem:

    def __init__(self):
        self.histories = []
        self.prices = []

    def setSeckillItem(self, item):

        # Basic
        self.wid = item.wareId
        self.name = item.wname

        # Prices
        self.price = item.miaoShaPrice
        self.histories.append(PriceHistory(price=float(item.jdPrice), time=datetime.now().strftime('%Y-%m-%d')))

        # Start and end times
        self.startTime = item.startTimeShow
        self.endTime = (item.endRemainTime - item.startRemainTime) / 3600

        # URL
        self.url = 'http://item.m.jd.com/product/%s.html' % item.wareId
        self.imageurl = item.imageurl

    def setHistories(self, histories):

        # Histories
        self.histories += histories

    def update(self):

        # Sort histories
        self.histories.sort(key=attrgetter('time'))

        # Calculate prices ratios
        prices = []
        self.totalDays = 0

        size = len(self.histories)

        for i in range(0, size):

            history = self.histories[i]
            days = 1

            if i < size - 1:
                thisDate = datetime.strptime(history.time, '%Y-%m-%d')
                nextDate = datetime.strptime(self.histories[i+1].time, '%Y-%m-%d')

                days = (nextDate - thisDate).days

            self.totalDays += days

            prices.append((history.price, days))

        prices.sort()

        pos = -1
        for price in prices:
            if pos >= 0 and self.prices[pos].price == price[0]:
                self.prices[pos].days += price[1]
                self.prices[pos].ratio = float(self.prices[pos].days) / float(self.totalDays)
            else:
                self.prices.append(Price(price[0], price[1], float(price[1]) / float(self.totalDays)))
                pos += 1

        # Calculate prices and discounts
        self.lowestPrice = float(int(100 * self.prices[0].price)) / 100

        self.avgPrice = 0.0
        for price in self.prices:
            self.avgPrice += float(price.price) * price.ratio

        self.avgPrice = float(int(100 * self.avgPrice)) / 100

        # Calculate discounts
        self.discount = int(100 * float(self.price) / float(self.avgPrice))
        if 0 == self.discount:
            self.discount = 1

        self.lowestRatio = int(100 * float(self.lowestPrice) / float(self.avgPrice))

        # Calculate weights
        lowestDiscount = int(100 * float(self.price) / float(self.lowestPrice))
        self.weight = lowestDiscount / float(self.totalDays)

    def __repr__(self):
        fields = ['    {}={}'.format(k, v)
            for k, v in self.__dict__.items()
                if not k.startswith('_') and 'histories' != k and 'prices' != k]

        str = ''
        for history in self.histories:
            str += '{}\n'.format(history)

        for price in self.prices:
            str += '{}\n'.format(price)

        return '{}:\n{}\n{}'.format(self.__class__.__name__, '\n'.join(fields), str)

    def __lt__(self, other):
        return (self.weight < other.weight)

    def __gt__(self, other):
        return (self.weight > other.weight)

class WareDisplayer:

    def outputHtml(self, ware):

        maxRatio = 80

        # Discount
        self.discount = maxRatio * ware.discount / 100

        # Let a small discount look a little bigger
        if self.discount < 2: self.discount += 2

        # Lowest Ratio
        self.lowestRatio = maxRatio * ware.lowestRatio / 100

        # Average Ratio
        self.avgRatio = maxRatio

        # Padding
        self.padding = 5
        if self.discount < 10: self.padding = 10

        if self.discount <= self.lowestRatio:
            with open('html/ware.html') as fp:
                template = fp.read()
                return template.format(ware, self)

        return None




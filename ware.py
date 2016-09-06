import math

import sys
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
        self.totalDays = 0
        self.lowestPrice = 0.0
        self.avgPrice = 0.0
        self.discount = 100
        self.lowestRatio = 100
        self.weight = sys.maxsize

    def setSeckillItem(self, item, matchesItem):

        # Basic
        self.wid = item.wareId

        if item.wname:
            self.name = item.wname.replace('\n', ' ').replace('\r', ' ').replace('\"', '`').replace('\'', '`')
        else:
            self.name = ''

        # Prices
        self.price = item.miaoShaPrice
        self.histories.append(PriceHistory(price=float(item.jdPrice), time=datetime.now().strftime('%Y-%m-%d')))

        # Start and end times
        self.startTime = matchesItem.startTime
        self.endTime = matchesItem.endTime

        # URLs
        self.baseUrl = 'http://item.jd.com/%s.html' % item.wareId # For history searching
        self.url = 'http://wq.jd.com/item/view?sku=%s' % item.wareId
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
        '''
        Weight should be measured by factors as following:
        1, discount relative to lowest prices
        2, discount relative to average prices
        3, off amount
        4, days
        '''
        lowestDiscount = float(self.price) / float(self.lowestPrice)

        lg = math.log(self.totalDays)
        if 0 == lg: lg = 0.1 # Log(1) is 0.0

        self.weight = lowestDiscount / lg

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

    def prepareHtml(self, ware):

        if ware.discount > ware.lowestRatio:
            return False

        if ware.totalDays < 30: # Less than one month
            return False

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

        # Colors
        if ware.totalDays < 30:
            self.totalDaysColor = 'rgb(255, 57, 31)'
        elif ware.totalDays < 60:
            self.totalDaysColor = 'rgb(255, 169, 33)'
        elif ware.totalDays < 90:
            self.totalDaysColor = 'rgb(5, 157, 127)'
        else:
            self.totalDaysColor = '#666'

        # Total days
        if ware.totalDays >= 365:
            self.totalDays = ">{}".format(ware.totalDays)
        else:
            self.totalDays = ware.totalDays

        return True

    def outputJson(self, ware):

        if not self.prepareHtml(ware):
            return None

        with open('json/ware.json') as fp:
            template = fp.read()
            return '{' + template.format(ware, self) + '}'

        return None

    def outputHtml(self, ware):

        if not self.prepareHtml(ware):
            return None

        with open('html/ware.html') as fp:
            template = fp.read()
            return template.format(ware, self)

        return None

    def outputMarkdown(self, ware, count):

        if ware.discount > ware.lowestRatio:
            return None

        if ware.totalDays < 30: # Less than one month
            return None

        # Total days
        if ware.totalDays >= 365:
            self.totalDays = ">{}".format(ware.totalDays)
        else:
            self.totalDays = ware.totalDays

        with open('markdown/ware.md') as fp:
            template = fp.read()
            return template.format(ware, self, count+1)

        return None


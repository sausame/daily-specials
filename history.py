import json
from ware import PriceHistory

class ThisPrice:

    def __init__(self, dictObj):
        self.set(dictObj)

    def set(self, dictObj):
        self.price = dictObj.pop("price")
        self.priceunit = dictObj.pop("priceunit")
        self.priceunitSymbol = dictObj.pop("priceunitSymbol")
        self.available = dictObj.pop("available")
        self.updateTime = dictObj.pop("updateTime")

    def __repr__(self):
        fields = ['  {}={}'.format(k, v)
            for k, v in self.__dict__.items() if not k.startswith("_")]

        return "{}:\n{}".format(self.__class__.__name__, '\n'.join(fields))

class ThisItem:

    def __init__(self, dictObj):
        self.set(dictObj)

    def set(self, dictObj):
        self.itemId = dictObj.pop("id")
        self.price = dictObj.pop("price")
        self.updateTime = dictObj.pop("updateTime")
        self.cpsUrl = dictObj.pop("cpsUrl")
        self.categoryId = dictObj.pop("categoryId")
        self.name = dictObj.pop("name")
        self.rebate = dictObj.pop("rebate")
        self.available = dictObj.pop("available")
        self.shortName = dictObj.pop("shortName")
        self.url = dictObj.pop("url")
        self.priceImageUrl = dictObj.pop("priceImageUrl")

    def __repr__(self):
        fields = ['  {}={}'.format(k, v)
            for k, v in self.__dict__.items() if not k.startswith("_")]

        return "{}:\n{}".format(self.__class__.__name__, '\n'.join(fields))

class PriceHistoryData:

    def __init__(self, dictObj):
        self.set(dictObj)

    def set(self, dictObj):
        self.curTime = dictObj.pop("curTime")
        self.startTime = dictObj.pop("startTime")
        self.histories = [PriceHistory(**history) for history in dictObj["list"]]

    def __repr__(self):

        fields = ['  {}={!r}'.format(k, v)
            for k, v in self.__dict__.items() if not k.startswith("_") and 'histories' != k]

        str = ''
        for history in self.histories:
            str += '{}\n'.format(history)

        return "{}:\n{}\n{}".format(self.__class__.__name__, '\n'.join(fields), str)


class HhHistoryParser:

    def __init__(self):
        pass

    def parse(self, path):

        def getJsonString(path):

            try:
                with open(path) as fh:
                    for line in fh.readlines(): 
                        if len(line) > 1024:

                            start = line.find('{')
                            end = line.rfind('}')

                            return line[start:end+1]
            except IOError:
                pass

            return None

        data = getJsonString(path)

        if not data:
            print 'Wrong format: {}'.format(path)
            return None

        self.obj = json.loads(data)

        return self.obj

    def getThisPrice(self):

        try:
            return ThisPrice(self.obj['thisPrice'])
        except KeyError:
            pass

        return None

    def getThisItem(self):

        try:
            return ThisItem(self.obj["thisItem"])
        except KeyError:
            pass

        return None

    def getHistoryData(self):

        try:
            return PriceHistoryData(self.obj["priceHistoryData"])
        except KeyError:
            pass

        return None




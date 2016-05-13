import json

class SeckillItem:

    def __init__(self, **kwargs):
        self.set(**kwargs)

    def set(self, **kwargs):
        for keyword in ["wareId", "wname", "imageurl", "jdPrice", "soldRate",
            "spuId", "rate", "startRemainTime", "endRemainTime",
            "miaoShaPrice", "discount", "tagType", "tagText",
            "clockNum", "startTimeShow", "resultSort"]:

            value = ""
            try:
                value = kwargs[keyword]
            except KeyError:
                pass
            finally:
                setattr(self, keyword, value)
            '''
            try:
                setattr(self, keyword, kwargs[keyword])
            except KeyError:
                pass
            '''

    def __repr__(self):
        fields = ['    {}={}'.format(k, v)
            for k, v in self.__dict__.items() if not k.startswith("_")]

        return "  {}:\n{}".format(self.__class__.__name__, '\n'.join(fields))

class SeckillInfo:

    def __init__(self, path):
        self.parse(path)

    def set(self, dictObj):
        self.timeRemain = dictObj.pop("timeRemain")
        self.itemList = [SeckillItem(**item) for item in dictObj["itemList"]]

    def __repr__(self):

        fields = ['  {}={!r}'.format(k, v)
            for k, v in self.__dict__.items() if not k.startswith("_") and 'itemList' != k]

        str = ''
        for item in self.itemList:
            str += '{}\n'.format(item)

        return "{}:\n{}\n{}".format(self.__class__.__name__, '\n'.join(fields), str)

    def parse(self, path):

        def getJsonString(path):

            with open(path) as fh:
                return 0, fh.read()

            return -1, ""

        ret, data = getJsonString(path)

        if ret < 0:
            print 'Wrong format: {}'.format(path)
            return

        obj = json.loads(data)
        self.set(obj["seckillInfo"])


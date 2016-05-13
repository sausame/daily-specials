import spidermonkey

class JsExecutor:

    def __init__(self, filename):

        def loadfile(filename):
            fp = open(filename)
            content = fp.read()
            fp.close()
            return content

        self.rt = spidermonkey.Runtime()
        self.cx = self.rt.new_context()
        self.cx.add_global("loadfile", loadfile)
        self.fname = filename

    def execute(self, value):
        command = 'var contents = loadfile("{}"); eval(contents); var content = {}; content;'.format(
            self.fname, value)

        return self.cx.execute(command)


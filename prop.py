
def getProperty(path, name):

    fp = None

    try:
        fp = open(path)

        minlen = len(name) + 1

        for line in fp:
            if len(line) < minlen or '#' == line[0]:
                continue

            group = line.strip().split('=')

            if 2 != len(group) or group[0].strip() != name:
                continue

            return group[1].strip()

    except IOError:
        pass

    finally:
        if fp != None: fp.close()

    return None


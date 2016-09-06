import os
import time

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

def removeOverdueFiles(pathname, seconds):

    now = time.time()

    for parent, dirnames, filenames in os.walk(pathname):

        for filename in filenames:

            path = parent + filename

            if now > os.path.getctime(path) + seconds:
                # Remove
                os.remove(path)


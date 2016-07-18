import httplib  
import socket

def saveHttpData(filename, url, host=None):

    if None == host:
        start = url.find('//') + 2
        end = url[start:].find('/')

        host = url[start:start+end]
        url = url[start+end:]

    for i in range(0, 3):
        conn = httplib.HTTPConnection(host, timeout=10)  
        conn.request("GET", url)

        try:
            res = conn.getresponse()
        except socket.timeout:
            conn.close()
            continue

        if 200 != res.status:
            print res.status, res.reason
            conn.close()
            continue

        data = res.read()
        conn.close()

        fp = open(filename, 'w')
        fp.write(data)
        fp.close()

        return 0

    return -1


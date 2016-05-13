import httplib  

def saveHttpData(filename, url, host=None):

    if None == host:
        start = url.find('//') + 2
        end = url[start:].find('/')

        host = url[start:start+end]
        url = url[start+end:]

    conn = httplib.HTTPConnection(host)  
    conn.request("GET", url)
    res = conn.getresponse()

    if 200 != res.status:
        print res.status, res.reason
        conn.close()
        return -1

    data = res.read()
    conn.close()

    fp = open(filename, 'w')
    fp.write(data)
    fp.close()

    return 0 


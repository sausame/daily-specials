import ftplib

def uploadFtp(host, dirname, path, user=None, passwd=None, isProtected=False):

    def upload(host, dirname, path, user, passwd, isProtected):

        ret = False

        try:
            if isProtected:
                if user and passwd:
                    ftp = ftplib.FTP_TLS(host, user, passwd)
                else:
                    ftp = ftplib.FTP_TLS(host)
            else:
                if user and passwd:
                    ftp = ftplib.FTP(host, user, passwd)
                else:
                    ftp = ftplib.FTP(host)

        except Exception, e:
            print 'Failed to connect host "%s" with' % host, user, 'and', passwd, ":", e
            return ret

        print 'Connected to host "%s" with' % host, user, 'and', passwd

        try:
            ftp.login()
        except Exception, e:
            print 'Failed to login:', e
            '''
            Do nothing because loginned failure is also raised here.
            '''

        if isProtected:
            print 'Switch to security communications'
            ftp.prot_p()

        try:
            pos = path.rindex('/')
            pos += 1
        except ValueError:
            pos = 0

        filename = path[pos:]

        try:
            ftp.cwd(dirname)
            ftp.storbinary('STOR %s' % filename, open(path, 'rb'))

        except Exception, e:
            print 'Failed to upload "%s" of "%s" to "%s":' % (filename, path, dirname), e

        else:
            print 'Uploaded "%s" of "%s" to "%s".' % (filename, path, dirname)
            ret = True

        ftp.quit()

        return ret

    '''
    In uploadFtp()
    '''

    for i in range(0, 3):
        ret = upload(host, dirname, path, user, passwd, isProtected)
        if ret: break;

        print 'Try it again. NO. %d' % (i + 1)


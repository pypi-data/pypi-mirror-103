from os import mkdir, unlink
from os.path import expanduser, join, exists
from click import secho

usrHome = expanduser('~')
xbimerHome = join(usrHome, '.xbimer')
xbimerFile = join(xbimerHome, '.cli')


def setToken(token):
    if not exists(xbimerHome):
        mkdir(xbimerHome)

    with open(xbimerFile, 'w') as f:
        f.write(token)
        f.close()


def getToken():

    if not exists(xbimerFile):
        secho('Error: No tokens available!!', fg='red')
        return None

    with open(xbimerFile) as f:
        token = f.read()
        f.close()

    return token


def delToken():
    if exists(xbimerFile):
        unlink(xbimerFile)

# API Refrence https://github.com/xbimer/xbimer-docs


class Applet(object):
    def __init__(self):
        print('__init__')

    def __kill__(self):
        print('__kill__')

    def OnContextMenuHook(self, m):
        print('OnContextMenuHook')
from requests import get, post
from json import dumps
from click import secho
from __token__ import delToken

xirBaseUrl = 'https://www.xbimer.com'


def httpPost(path, *args, **kwargs):
    url = '/'.join([xirBaseUrl, path])
    data = kwargs.pop('data')
    headers = {'Content-Type': 'application/json'}
    kwargs.setdefault('headers', headers)
    kwargs.setdefault('data', dumps(data))
    reply = post(url, *args, **kwargs)
    try:
        reply.raise_for_status()
        return reply.json()
    except:
        if reply.status_code == 401:
            secho('Error: Token has expired!!!', fg='red')
            delToken()
        else:
            secho(reply.json()['message'], fg='red')
        return None


def httpGet(path, *args, **kwargs):
    url = '/'.join([xirBaseUrl, path])
    reply = get(url, *args, **kwargs)
    try:
        reply.raise_for_status()
        return reply.json()
    except:
        if reply.status_code == 401:
            secho('Error: Token has expired!!!', fg='red')
            delToken()
        else:
            secho(reply.json()['message'], fg='red')
        return None
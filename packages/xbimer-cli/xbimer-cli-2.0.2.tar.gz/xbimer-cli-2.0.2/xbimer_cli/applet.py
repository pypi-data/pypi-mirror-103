from click import command, option, secho
from __http__ import httpGet, httpPost
from __token__ import getToken
from __assets__ import ARCHICAD_SUPPORT, assetsCopy
from os.path import join, exists, isdir
from os import getcwd, mkdir
from json import dumps


@command()
@option('--name', prompt='What\'s applet name?')
def main(name):
    if len(name) < 4:
        secho('Error: name length must be greater than 4', fg='red')
        return

    if len(name) > 16:
        secho('The name length must be less than 16', fg='red')
        return

    token = getToken()
    if token is None:
        return

    appHome = join(getcwd(), name)
    if exists(appHome) and isdir(appHome):
        secho('The applet project directory already exists', fg='red')
        return

    app = httpPost('clis/applet', params={'token': token}, data={'name': name})
    if app is None:
        return

    latestReply = httpGet('open/releases/latest')
    if latestReply is None:
        return

    xirVersion = latestReply['xir']['version']

    # app['id]
    # app['sign']
    app['name'] = name
    app['runtime'] = xirVersion
    app['icon'] = 'default.png'
    app['main'] = 'main.py'
    app['version'] = '1.0.0'
    app['archicads'] = ARCHICAD_SUPPORT

    assetsCopy('applet', appHome)

    appManifest = join(appHome, 'manifest.json')
    with open(appManifest, 'w', encoding='utf-8') as f:
        f.write(dumps(app, indent=2, ensure_ascii=False))
        f.close()

from click import secho, command
from __http__ import httpGet
from semver import compare
from __version__ import CURRENT_VERSION


@command()
def main():
    secho('xbimer-cli ' + CURRENT_VERSION)


def updateCheck():
    reply = httpGet('open/releases/latest')

    if reply is None:
        return

    LATEST_VERSION = reply['cli']['version']
    if compare(LATEST_VERSION, CURRENT_VERSION) == 1:
        secho(
            f'WARNING: You are using xbimer-cli version {CURRENT_VERSION}, however version {LATEST_VERSION} is available.',
            fg='yellow')
        secho(
            f'You should consider upgrading via the \'pip install --upgrade xbimer-cli\' command.',
            fg='yellow')

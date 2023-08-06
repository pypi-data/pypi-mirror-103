from click import secho, command
from __token__ import getToken
from __http__ import httpGet


@command()
def main():
    token = getToken()

    if token is None:
        return

    info = httpGet('clis/whoami', params={'token': token})

    if info is None:
        return

    secho(f"The logged user is: {info['name']}")
    secho(f"The user github username is: {info['nickname']}")

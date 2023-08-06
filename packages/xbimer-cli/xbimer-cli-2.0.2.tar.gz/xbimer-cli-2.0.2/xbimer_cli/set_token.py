from click import command, argument, secho
from __token__ import setToken


@command()
@argument('token')
def main(token):
    setToken(token)
    secho('xbimer-token: ' + token + ' saved!!')

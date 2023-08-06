from os.path import dirname
from sys import path

here = dirname(__file__)
path.append(here)

import click

import version
import set_token
import whoami
import applet
import module


@click.group()
def main():
    version.updateCheck()


main.add_command(version.main, "version")
main.add_command(set_token.main, 'set-token')
main.add_command(whoami.main, 'whoami')
main.add_command(applet.main, 'applet-init')
main.add_command(module.main, 'module-init')

if __name__ == "__main__":
    main()

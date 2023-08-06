from click import command, option, secho
from os.path import join, isdir, exists
from os import getcwd
from __vsproj__ import initGuide


@command()
@option('--name', prompt='What\'s module name?')
@option('--usesdk', is_flag=True, prompt='Do you want to use native SDK?')
def main(name, usesdk):
    if len(name) < 4:
        secho('Error: name length must be greater than 4', fg='red')
        return

    moduleHome = join(getcwd(), name)
    if exists(moduleHome) and isdir(moduleHome):
        secho('The module project directory already exists', fg='red')
        return

    initGuide(moduleHome, name, usesdk)

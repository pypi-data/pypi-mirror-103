from os.path import join, dirname
from shutil import copytree
from zipfile import ZipFile

ARCHICAD_SUPPORT = [22, 23, 24]


def assetsCopy(srcName, destDir):
    here = dirname(__file__)
    srcHome = join(here, 'assets', srcName)
    copytree(srcHome, destDir)


def assetsExtract(srcName, destDir):
    here = dirname(__file__)
    srcHome = join(here, 'assets', 'ziplibs', f'{srcName}.zip')
    zFile = ZipFile(srcHome)
    zFile.extractall(destDir)

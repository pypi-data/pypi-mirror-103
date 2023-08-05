from os.path import dirname, abspath, join
import sys
from importlib import import_module

CURRENT_DIR = dirname(abspath(__file__)) + '/'
sys.path.append(CURRENT_DIR)
MODEL = 'ipcc2006Tier1'
PKG = join('hestia_earth', 'models', MODEL)


def run(model: str, data):
    run = getattr(import_module(f".{model}", package=PKG), 'run')
    return run(data)

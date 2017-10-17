from importlib import import_module


def load(path):
    mod = import_module(path)
    return getattr(mod, 'process')

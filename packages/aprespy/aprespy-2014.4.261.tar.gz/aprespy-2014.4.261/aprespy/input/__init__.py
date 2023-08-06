"""
"""
from input import z


def read(path: str):
    if path.endswith('zss') or path.endswith('zrr'):
        return z.read(path)

"""
"""
# try:
from aprespy.input import z
# except ImportError:



def read(path: str):
    if path.endswith('zss') or path.endswith('zrr'):
        return z.read(path)

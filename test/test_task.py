from novel.spiders import Spiders
from novel.setting import test_data
from os.path import dirname, join
from os import chdir
import sys

chdir(join(dirname(sys.path[0]), 'temp'))
if __name__ == '__main__':
    s = Spiders()
    s.task(test_data)

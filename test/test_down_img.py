from novel.spiders import Spiders
from os.path import dirname, join
from os import chdir
import sys

chdir(join(dirname(sys.path[0]), 'temp'))
if __name__ == '__main__':
    s = Spiders
    s.down_img('https://ekwing-resource.oss-cn-shanghai.aliyuncs.com/banner/2017/09/01/59a8f970bbf51.jpg', '')

#__author: busensei
#data: 2018/9/2


import sys
import os

path = os.path.abspath(__file__)
path = os.path.dirname(os.path.dirname(path))
sys.path.append(path)


from core import main


if __name__ == '__main__':
        main.ArgvHandler()
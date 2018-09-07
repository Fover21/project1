#__author: busensei
#data: 2018/8/3

import sys



path = __file__.split('/')
# print(path)  # ['', 'Users', 'busensei', 'wzy', 'OldBoy', 'Week05', 'Week05作业', 'student_selection_system', 'bin', 'start.py']
path = path[0:-2]
path = '/'.join(path)
# print(path)  #/Users/busensei/wzy/OldBoy/Week05/Week05作业/student_selection_system
sys.path.append(path)

from core import main

main.main()

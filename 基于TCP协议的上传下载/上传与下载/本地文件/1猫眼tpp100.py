#__author: busensei
#data: 2018/8/6


import requests
import re

base_url = 'http://maoyan.com/board/4?offset='

for i in range(10):
    i = str(i)
    if i == '0':
        i = base_url + i
    else:
        i = base_url + i + '0'

    response = requests.get(i)

    html = response.text

    pattern = re.compile('<dd>.*?title="(.*?)".*?<p class="star">(.*?)</p>.*?<p class="releasetime">(.*?)</p>.*?<i class="integer">(.*?)</i>.*?<i class="fraction">(.*?)</i>.*?</dd>', re.S)

    r = re.findall(pattern, html)
    print(r)

    # for i in r:
    #
    #     #print(i)
    #     for j in i:
    #         j = j.split()
    #         print(j, end=' ')
    #     print()#__author: busensei
#data: 2018/8/6


import requests
import re

base_url = 'http://maoyan.com/board/4?offset='

for i in range(10):
    i = str(i)
    if i == '0':
        i = base_url + i
    else:
        i = base_url + i + '0'

    response = requests.get(i)

    html = response.text

    pattern = re.compile('<dd>.*?title="(.*?)".*?<p class="star">(.*?)</p>.*?<p class="releasetime">(.*?)</p>.*?<i class="integer">(.*?)</i>.*?<i class="fraction">(.*?)</i>.*?</dd>', re.S)

    r = re.findall(pattern, html)
    print(r)

    # for i in r:
    #
    #     #print(i)
    #     for j in i:
    #         j = j.split()
    #         print(j, end=' ')
    #     print()#__author: busensei
#data: 2018/8/6


import requests
import re

base_url = 'http://maoyan.com/board/4?offset='

for i in range(10):
    i = str(i)
    if i == '0':
        i = base_url + i
    else:
        i = base_url + i + '0'

    response = requests.get(i)

    html = response.text

    pattern = re.compile('<dd>.*?title="(.*?)".*?<p class="star">(.*?)</p>.*?<p class="releasetime">(.*?)</p>.*?<i class="integer">(.*?)</i>.*?<i class="fraction">(.*?)</i>.*?</dd>', re.S)

    r = re.findall(pattern, html)
    print(r)

    # for i in r:
    #
    #     #print(i)
    #     for j in i:
    #         j = j.split()
    #         print(j, end=' ')
    #     print()#__author: busensei
#data: 2018/8/6


import requests
import re

base_url = 'http://maoyan.com/board/4?offset='

for i in range(10):
    i = str(i)
    if i == '0':
        i = base_url + i
    else:
        i = base_url + i + '0'

    response = requests.get(i)

    html = response.text

    pattern = re.compile('<dd>.*?title="(.*?)".*?<p class="star">(.*?)</p>.*?<p class="releasetime">(.*?)</p>.*?<i class="integer">(.*?)</i>.*?<i class="fraction">(.*?)</i>.*?</dd>', re.S)

    r = re.findall(pattern, html)
    print(r)

    # for i in r:
    #
    #     #print(i)
    #     for j in i:
    #         j = j.split()
    #         print(j, end=' ')
    #     print()
# coding=utf-8

# 引入外部库
import jieba
import re
from bs4 import BeautifulSoup

# 引入内部库
from Http.GetHttp import *

# 全局变量
URL = 'https://baike.baidu.com/item/%E6%9C%BA%E5%9C%BA/74273'
city_type = ['省', '市', '区', '县', '镇', '盟', '旗', '乡', '州']


def get_airport(airport_dict: dict) -> None:
    """

    :param airport_dict:
    :return:
    """
    page_content = GetHttp().get_page_content(URL, 3, charset='utf-8')
    if page_content:
        soup = BeautifulSoup(page_content, 'html.parser')
        for table in soup.find_all(attrs={'class': 'table-view'}):
            print('获取【省/直辖市/自治区】')
            for tr in table.find_all('tr')[1:]:
                tds = tr.find_all('td')
                airport = re.sub("[\[0-90-9\]]", "", tds[0].text.replace('\n', '').replace(' ', ''))

                pos = list(tds[1].text.replace('\n', '').replace(' ', ''))
                i = 0
                while i < len(pos)-1:
                    if pos[i][-1] not in city_type:
                        cur_pos = pos.pop(i)
                        pos[i] = cur_pos + pos[i]
                    elif pos[i+1][-1] in city_type:
                        cur_pos = pos.pop(i)
                        pos[i] = cur_pos + pos[i]
                    else:
                        i += 1
                print(pos)

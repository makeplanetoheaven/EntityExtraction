# coding=utf-8

# 引入外部库
from bs4 import BeautifulSoup

# 引入内部库
from Http.GetHttp import *

# 全局变量
URL = 'http://hcp.bendibao.com/station.html'


def get_train_station() -> [list, list]:
    page_content = GetHttp().get_page_content(URL, 3)
    entity_info = []
    entity_rel = []
    if page_content:
        soup = BeautifulSoup(page_content, 'html.parser')
        index = 0
        for city_list in soup.find_all(attrs={'class': 'citylist'}):
            for city_a in city_list.find_all('a'):
                city = city_a.text
                train_list = BeautifulSoup(
                    GetHttp().get_page_content(URL.replace('/station.html', '') + city_a.get('href'), 3),
                    'html.parser').find(attrs={'class': 'onecity'})
                for train_a in train_list.find_all('a'):
                    train_station = train_a.text + '站'
                    entity_info.append(
                        {'type': '火车站', 'property': {'name': train_station, '域': '地理位置域', 'id': 'CNT' + str(index)}})
                    entity_rel.append([index, '位于', city])
                    index += 1

    return entity_info, entity_rel

# coding=utf-8

# 引入外部库
import jieba
from bs4 import BeautifulSoup

# 引入内部库
from Http.GetHttp import *

# 全局变量
URL = 'https://baike.baidu.com/item/%E6%9C%BA%E5%9C%BA/74273'


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
                airport = tds[0].text.replace('\n', '').replace(' ', '')
                pos = tds[1].text.replace('\n', '').replace(' ', '')
                type = tds[2].text.replace('\n', '').replace(' ', '')
                # link_id = re.sub("\D", "", a.get('href'))

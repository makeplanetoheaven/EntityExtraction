# coding=utf-8

# 引入外部库
import os
import re
import sys
from bs4 import BeautifulSoup


# 引入内部库
from Http.GetHttp import *


# 全局变量
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
URL = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2018/'
HEADER = {'Cookie': 'AD_RS_COOKIE=20080917',
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \ AppleWeb\Kit/537.36 (KHTML, like Gecko)\ '
                        'Chrome/58.0.3029.110 Safari/537.36'}


def get_province(province_dict):
    """
    获取全国省份和直辖市
    :param province_dict: 用来存储所包含省的字典
    :return:
    """
    print('获取【省/直辖市】----------')
    http = GetHttp(URL, HEADER)
    page_content = http.get_page_content
    if page_content:
        soup = BeautifulSoup(page_content, 'html.parser')
        for i in soup.find_all(attrs={'class': 'provincetr'}):
            for a in i.find_all('a'):
                link_id = re.sub("\D", "", a.get('href'))
                province_dict[link_id] = {'id': link_id, 'name': a.text}


def get_city(province_dict):
    """
    获取每所有省的下级市
    :param province_dict:用来存储所包含省的字典
    :return:
    """
    print('获取【市/市辖区】----------')
    for province_id in province_dict:
        city_dict = {}

        page_content = GetHttp(URL + province_id + '.html', HEADER).get_page_content
        if not page_content:
            continue
        soup = BeautifulSoup(page_content, 'html.parser')
        for city_item in soup.find_all(attrs={'class': 'citytr'}):
            city_id = str(city_item.find_all('td')[0].text)
            if city_id[0:4] not in city_dict:
                city_dict[city_id[0:4]] = {'id': city_id[0:4], 'name': str(city_item.find_all('td')[1].text)}

        province_dict[province_id]['city'] = city_dict


def get_county(province_dict):
    """
    获取所有市的下级县区
    :param province_dict:用来存储所包含省的字典
    :return:
    """
    print('获取【县/区】----------')
    for province_id in province_dict:
        city_dict = province_dict[province_id]['city']
        for city_id in city_dict:
            county_dict = {}

            page_content = GetHttp(URL + city_id[0:2] + '/' + city_id + '.html', HEADER).get_page_content
            if not page_content:
                continue
            soup = BeautifulSoup(page_content, 'html.parser')
            for county_item in soup.find_all(attrs={'class': 'countytr'}):
                county_id = str(county_item.find_all('td')[0].text)
                if county_id[0:6] not in county_dict:
                    county_dict[county_id[0:6]] = {'id': county_id[0:6],
                                                   'name': str(county_item.find_all('td')[1].text)}

            city_dict[city_id]['county'] = county_dict


def get_town(province_dict):
    """
    获取县区的下级镇、街道
    :param province_dict:
    :return:
    """
    print('获取【镇/乡/办事处/街道】----------')
    for province_id in province_dict:
        for city_id in province_dict[province_id]['city']:
            county_dict = province_dict[province_id]['city'][city_id]
            for county_id in county_dict:
                town_dict = {}

                page_content = GetHttp(URL + county_id[0:2] + '/' + county_id[2:4] + '/' + county_id + '.html',
                                       HEADER).get_page_content
                if not page_content:
                    continue
                soup = BeautifulSoup(page_content, 'html.parser')
                for town_item in soup.find_all(attrs={'class': 'towntr'}):
                    town_id = str(town_item.find_all('td')[0].text)
                    if town_id[0:9] not in town_dict:
                        town_dict[town_id[0:9]] = {'id': town_id[0:9], 'name': str(town_item.find_all('td')[1].text)}

                county_dict[county_id]['town'] = town_dict


def get_village(province_dict):
    # 镇下级村
    print('获取【村/委员会】----------')
    for province_id in province_dict:
        for city_id in province_dict[province_id]['city']:
            for county_id in province_dict[province_id]['city'][city_id]['county']:
                town_dict = province_dict[province_id]['city'][city_id]['county'][county_id]
                for town_id in town_dict:
                    village_dict = {}

                    page_content = GetHttp(
                        URL + town_id[0:2] + '/' + town_id[2:4] + '/' + town_id[4:6] + '/' + town_id + '.html',
                        HEADER).get_page_content
                    if not page_content:
                        continue
                    soup = BeautifulSoup(page_content, 'html.parser')
                    for village_item in soup.find_all(attrs={'class': 'villagetr'}):
                        village_id = str(village_item.find_all('td')[0].text)
                        if village_id[0:12] not in village_dict:
                            village_dict[village_id[0:12]] = {'id': village_id[0:12],
                                                              'name': str(village_item.find_all('td')[1].text)}

                    town_dict[town_id]['village'] = village_dict


result_dict = {}
get_province(result_dict)
get_city(result_dict)
get_county(result_dict)
get_town(result_dict)
get_village(result_dict)

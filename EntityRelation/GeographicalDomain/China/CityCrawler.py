# coding=utf-8

# 引入外部库
import time
import os
import re
import sys
from bs4 import BeautifulSoup

# 引入内部库
from Http.GetHttp import *

# 全局变量
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
URL = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2018/'


def get_province (province_dict: dict) -> None:
	"""
	获取全国省份和直辖市
	:param province_dict: 用来存储包含省的字典
	:return: None
	"""
	print('获取【省/直辖市/自治区】----------')
	page_content = GetHttp().get_page_content(URL, 3)
	if page_content:
		soup = BeautifulSoup(page_content, 'html.parser')
		for i in soup.find_all(attrs={'class': 'provincetr'}):
			for a in i.find_all('a'):
				link_id = re.sub("\D", "", a.get('href'))
				province_dict[link_id] = {'id': link_id, 'name': a.text}


def get_city (province_dict: dict) -> None:
	"""
	获取每所有省的下级市
	:param province_dict: 用来存储包含省的字典
	:return: None
	"""
	print('获取【市/市辖区/自治州】----------')
	for province_id in province_dict:
		city_dict = {}

		page_content = GetHttp().get_page_content(URL + province_id + '.html', 3)
		if not page_content:
			continue
		soup = BeautifulSoup(page_content, 'html.parser')
		for city_item in soup.find_all(attrs={'class': 'citytr'}):
			city_id = str(city_item.find_all('td')[0].text)
			if city_id[0:4] not in city_dict:
				city_dict[city_id[0:4]] = {'id': city_id[0:4], 'name': str(city_item.find_all('td')[1].text)}

		province_dict[province_id]['city'] = city_dict


def get_county (province_dict: dict) -> None:
	"""
	获取所有市的下级县区
	:param province_dict: 用来存储包含省的字典
	:return: None
	"""
	print('获取【县/区/自治县】----------')
	for province_id in province_dict:
		city_dict = province_dict[province_id]['city']
		for city_id in city_dict:
			county_dict = {}

			page_content = GetHttp().get_page_content(URL + city_id[0:2] + '/' + city_id + '.html', 3)
			if not page_content:
				continue
			soup = BeautifulSoup(page_content, 'html.parser')
			for county_item in soup.find_all(attrs={'class': 'countytr'}):
				county_id = str(county_item.find_all('td')[0].text)
				if county_id[0:6] not in county_dict:
					county_dict[county_id[0:6]] = {'id': county_id[0:6],
					                               'name': str(county_item.find_all('td')[1].text)}

			city_dict[city_id]['county'] = county_dict


def get_town (province_dict: dict) -> None:
	"""
	获取县区的下级镇、街道
	:param province_dict: 用来存储包含省的字典
	:return: None
	"""
	print('获取【镇/乡/办事处/街道】----------')
	for province_id in province_dict:
		for city_id in province_dict[province_id]['city']:
			county_dict = province_dict[province_id]['city'][city_id]['county']
			for county_id in county_dict:
				town_dict = {}

				page_content = GetHttp().get_page_content(
					URL + county_id[0:2] + '/' + county_id[2:4] + '/' + county_id + '.html', 3)
				if not page_content:
					continue
				soup = BeautifulSoup(page_content, 'html.parser')
				for town_item in soup.find_all(attrs={'class': 'towntr'}):
					town_id = str(town_item.find_all('td')[0].text)
					if town_id[0:9] not in town_dict:
						town_dict[town_id[0:9]] = {'id': town_id[0:9], 'name': str(town_item.find_all('td')[1].text)}

				county_dict[county_id]['town'] = town_dict


def get_village (province_dict: dict) -> None:
	"""
	获取镇、街道下级的村、委员会
	:param province_dict: 用来存储包含省的字典
	:return: None
	"""
	# 镇下级村
	print('获取【村/委员会】----------')
	for province_id in province_dict:
		for city_id in province_dict[province_id]['city']:
			for county_id in province_dict[province_id]['city'][city_id]['county']:
				town_dict = province_dict[province_id]['city'][city_id]['county'][county_id]['town']
				for town_id in town_dict:
					village_dict = {}

					page_content = GetHttp().get_page_content(
						URL + town_id[0:2] + '/' + town_id[2:4] + '/' + town_id[4:6] + '/' + town_id + '.html', 3)
					if not page_content:
						continue
					soup = BeautifulSoup(page_content, 'html.parser')
					for village_item in soup.find_all(attrs={'class': 'villagetr'}):
						village_id = str(village_item.find_all('td')[0].text)
						if village_id[0:12] not in village_dict:
							village_dict[village_id[0:12]] = {'id': village_id[0:12],
							                                  'name': str(village_item.find_all('td')[1].text)}

					town_dict[town_id]['village'] = village_dict


def format_conversion (province_dict: dict) -> [list, list]:
	"""
	关系类型：
	节点类型：
	:param province_dict:
	:return:
	"""
	entity_info = [{'type': '国家', 'property': {'name': '中国', '域': '地理位置域'}}]
	entity_rel = []

	# 国家与省关系
	shoudu = True
	for province_id in province_dict:
		province = province_dict[province_id]
		province_type = '省份'
		if '市' in province['name']:
			province_type = '直辖市'
		elif '自治区' in province['name']:
			province_type = '自治区'
		entity_info.append({'type': province_type, 'property': {'name': province['name'], '域': '地理位置域'}})
		entity_rel.append(['中国', {'name': '包含', 'property': {}}, province['name']])
		if shoudu:
			shoudu = False
			entity_rel.append(['中国', {'name': '首都', 'property': {}}, province['name']])
		entity_rel.append([province['name'], {'name': '属于', 'property': {}}, '中国'])

		# 省与市关系
		for city_id in province['city']:
			city = province['city'][city_id]

	return entity_info, entity_rel

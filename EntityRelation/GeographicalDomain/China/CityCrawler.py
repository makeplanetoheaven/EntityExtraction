# coding=utf-8

# 引入外部库
import re
from bs4 import BeautifulSoup

# 引入内部库
from Http.GetHttp import *

# 全局变量
URL = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2018/'


def get_province (province_dict: dict) -> None:
	"""
	获取全国省份和直辖市
	:param province_dict: 用来存储包含省的字典
	:return: None
	"""
	print('获取【省/直辖市/自治区】')
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
	print('获取【市/市辖区/自治州/地区/直辖县】')
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
	print('获取【县/区/自治县/县级市】')
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
				if county_id[0:6] not in county_dict and str(county_item.find_all('td')[1].text) != '市辖区':
					county_dict[county_id[0:6]] = {'id': county_id[0:6],
					                               'name': str(county_item.find_all('td')[1].text)}

			city_dict[city_id]['county'] = county_dict


def get_town (province_dict: dict) -> None:
	"""
	获取县区的下级镇、街道
	:param province_dict: 用来存储包含省的字典
	:return: None
	"""
	print('获取【镇/乡/街道/开发区】')
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
	print('获取【村/委员会】')
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
							                                  'name': str(village_item.find_all('td')[2].text)}

					town_dict[town_id]['village'] = village_dict


def format_conversion (province_dict: dict) -> [list, list]:
	"""
	关系类型：首都、省会、包含、属于
	:param province_dict:
	:return: entity_info, entity_rel
	"""
	print('开始转换格式------')
	entity_info = [{'type': '国家', 'property': {'name': '中国', '域': '地理位置域'}}]
	entity_index = {'中国': 0}
	index = 1
	entity_rel = []

	# 国家与省关系
	shou_du = True
	for province_id in province_dict:
		province = province_dict[province_id]
		province_type = '省份'
		if '市' in province['name']:
			province_type = '直辖市'
		elif '自治区' in province['name']:
			province_type = '自治区'
		entity_info.append({'type': province_type, 'property': {'name': province['name'], '域': '地理位置域'}})
		entity_index[province['name']] = index
		index += 1
		entity_rel.append(['中国', {'name': '包含', 'property': {}}, province['name']])
		if shou_du:
			shou_du = False
			entity_rel.append(['中国', {'name': '首都', 'property': {}}, province['name']])
		entity_rel.append([province['name'], {'name': '属于', 'property': {}}, '中国'])

		# 省与市关系
		sheng_hui = True
		for city_id in province['city']:
			city = province['city'][city_id]
			city_type = '市'
			if '市辖区' in city['name']:
				city_type = '市辖区'
			elif '自治州' in city['name']:
				city_type = '自治州'
			elif '地区' in city['name']:
				city_type = '地区'
			elif '直辖县' in city['name']:
				city_type = '直辖县'
			entity_info.append({'type': city_type, 'property': {'name': city['name'], '域': '地理位置域'}})
			entity_index[city['name']] = index
			index += 1
			entity_rel.append([province['name'], {'name': '包含', 'property': {}}, city['name']])
			if sheng_hui:
				sheng_hui = False
				entity_rel.append([province['name'], {'name': '省会', 'property': {}}, city['name']])
			entity_rel.append([city['name'], {'name': '属于', 'property': {}}, province['name']])

			# 市与县关系
			for county_id in city['county']:
				county = city['county'][county_id]
				county_type = '县'
				if '区' in county['name']:
					county_type = '区'
				elif '自治县' in county['name']:
					county_type = '自治县'
				elif '市' in county['name']:
					county_type = '县级市'
				entity_info.append({'type': county_type, 'property': {'name': county['name'], '域': '地理位置域'}})
				entity_index[county['name']] = index
				index += 1
				entity_rel.append([city['name'], {'name': '包含', 'property': {}}, county['name']])
				entity_rel.append([county['name'], {'name': '属于', 'property': {}}, city['name']])

				# 县与镇关系
				for town_id in county['town']:
					town = county['town'][town_id]
					town_type = '镇'
					if '乡' in town['name']:
						town_type = '乡'
					elif '街道' in town['name']:
						town_type = '街道'
					elif '开发区' in town['name']:
						town_type = '开发区'
					entity_info.append({'type': town_type, 'property': {'name': town['name'], '域': '地理位置域'}})
					entity_index[town['name']] = index
					index += 1
					entity_rel.append([county['name'], {'name': '包含', 'property': {}}, town['name']])
					entity_rel.append([town['name'], {'name': '属于', 'property': {}}, county['name']])

					# 镇与村关系
					for village_id in town['village']:
						village = town['village'][village_id]
						village_type = '村'
						if '委员会' in village['name']:
							village_type = '委员会'
						entity_info.append({'type': village_type, 'property': {'name': village['name'], '域': '地理位置域'}})
						entity_index[village['name']] = index
						index += 1
						entity_rel.append([town['name'], {'name': '包含', 'property': {}}, village['name']])
						entity_rel.append([village['name'], {'name': '属于', 'property': {}}, town['name']])

	print('中国一共有' + str(index - 1) + '个城市')
	# 序号转换
	print('开始转换序号------')
	for i in range(len(entity_rel)):
		entity_rel[i][0] = entity_index[entity_rel[i][0]]
		entity_rel[i][2] = entity_index[entity_rel[i][2]]

	return entity_info, entity_rel

# coding=utf-8

# 引入外部库
import re

# 引入内部库
from EntityInformation.BaiduEncyclopedia import *

# 全局变量
data_path = './EntityRelation/GeographicalDomain/China/Data/中国山脉及山峰.txt'


def get_mountain () -> [list, list]:
	"""

	:return:
	"""
	# 数据读取
	mountain_dict = {}
	letter_pattern = re.compile('[A-Z]')
	with open(data_path, 'r', encoding='utf-8') as file_objct:
		for line in file_objct:
			if not letter_pattern.findall(line):
				temp = line.rstrip('\n').split(' ')
				mountain_dict[temp[0]] = {}
				for i in range(1, len(temp)):
					mountain_dict[temp[0]][temp[i]] = 1

	brackets_pattern = re.compile('（(.*?)）')
	entity_info = []
	entity_rel = []
	# 构建内部关系
	for ridge in mountain_dict:
		ridge_index = len(entity_info)
		entity_info.append({'type': '山脉', 'property': {'name': brackets_pattern.sub('', ridge), '域': '地理位置域',
		                                               'id': 'CNM' + str(ridge_index)}})
		if brackets_pattern.findall(ridge):
			ridges = brackets_pattern.search(ridge).group(0).rstrip('）').lstrip('（').split('，')
			for temp in ridges:
				entity_rel.append([ridge_index, {'name': '包含', 'property': {}}, len(entity_info)])
				entity_rel.append([len(entity_info), {'name': '属于', 'property': {}}, ridge_index])
				entity_info.append(
					{'type': '山脉', 'property': {'name': temp, '域': '地理位置域', 'id': 'CNM' + str(len(entity_info))}})
		for peak in mountain_dict[ridge]:
			peak_index = len(entity_info)
			entity_rel.append([ridge_index, {'name': '包含', 'property': {}}, peak_index])
			entity_rel.append([peak_index, {'name': '属于', 'property': {}}, ridge_index])
			if brackets_pattern.findall(peak):
				entity_info.append({'type': '山群', 'property': {'name': brackets_pattern.sub('', peak), '域': '地理位置域',
				                                               'id': 'CNM' + str(peak_index)}})
				peaks = brackets_pattern.search(peak).group(0).rstrip('）').lstrip('（').split('，')
				for temp in peaks:
					entity_rel.append([peak_index, {'name': '包含', 'property': {}},  len(entity_info)])
					entity_rel.append([ len(entity_info), {'name': '属于', 'property': {}}, peak_index])
					entity_info.append(
						{'type': '山峰', 'property': {'name': temp, '域': '地理位置域', 'id': 'CNM' + str(len(entity_info))}})
			else:
				entity_info.append(
					{'type': '山峰', 'property': {'name': peak, '域': '地理位置域', 'id': 'CNM' + str(peak_index)}})

	# 构建外部关系
	for entity in entity_info:
		entity_info_extract(entity['property'])

	print(entity_info)

	return entity_info, entity_rel

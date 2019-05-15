# coding=utf-8

# 引入外部库
import re
from bs4 import BeautifulSoup

# 引入内部库
from Http.GetHttp import *

# 全局变量
URL = 'https://baike.baidu.com/item/'


def entity_info_extract (entity_property: dict) -> None:
	"""
	根据所传入的实体属性字典，从百度百科上获取与实体名对应的基本信息和属性
	注意：只能处理非多义词实体
	:param entity_property: 实体属性字典
	:return: None
	"""
	page_content = GetHttp().get_page_content(URL + entity_property['name'], 3, charset='utf-8')
	soup = BeautifulSoup(page_content, 'html.parser')

	# summary
	summary = ''
	summary_tag = soup.find(attrs={'class': 'lemma-summary'})
	if summary_tag:
		for para in summary_tag.find_all(attrs={'class': 'para'}):
			summary += para.text.replace('\n', '').replace(' ', '')
		entity_property['介绍'] = summary
	else:
		print('实体[%s]介绍缺失！' % entity_property['name'])

	# basic info
	basic_info_tag = soup.find(attrs={'class': 'basic-info'})
	if basic_info_tag:
		name_list = basic_info_tag.find_all(attrs={'class': 'name'})
		value_list = basic_info_tag.find_all(attrs={'class': 'value'})
		for i in range(len(name_list)):
			entity_property[name_list[i].text.replace('\n', '').replace(' ', '')] = \
				value_list[i].text.replace('\n', '').replace(' ', '')
	else:
		print('实体[%s]基本属性缺失！' % entity_property['name'])

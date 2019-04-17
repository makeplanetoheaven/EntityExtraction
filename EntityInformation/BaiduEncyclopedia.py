# coding=utf-8

# 引入外部库
import re
from bs4 import BeautifulSoup

# 引入内部库
from Http.GetHttp import *


# 全局变量
URL = 'https://baike.baidu.com/item/'


def entity_info_extract (entity_property: dict):
	page_content = GetHttp().get_page_content(URL + entity_property['name'], 3, charset='utf-8')
	if page_content:
		soup = BeautifulSoup(page_content, 'html.parser')
		print(page_content)
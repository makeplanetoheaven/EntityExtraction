# coding=utf-8

# 引入外部库
import sys
import os
import re
from urllib import request
from bs4 import BeautifulSoup

# 引入内部库


# 全局变量
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
url = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2018/'
header = {'Cookie': 'AD_RS_COOKIE=20080917',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \ AppleWeb\Kit/537.36 (KHTML, like Gecko)\ '
	              'Chrome/58.0.3029.110 Safari/537.36'}


class GetHttp:
	def __init__ (self, url, headers=None, charset='utf-8'):
		if headers is None:
			headers = {}
		self._response = ''
		try:
			self._response = request.urlopen(request.Request(url=url, headers=headers))
		except Exception as e:
			print(e)
		self._c = charset

	@property
	def text (self):
		try:
			return self._response.read().decode(self._c)
		except Exception as e:
			print(e)
			return ''


def get_province (url, header):
	"""
	获取全国省份和直辖市
	:param url: url地址
	:param header: 请求头
	:return: province_dict:匹配到的省和直辖市结果字典
	"""
	province_dict = {}
	page_content = GetHttp(url, header).text
	if page_content:
		soup = BeautifulSoup(page_content, 'html.parser')
		for i in soup.find_all(attrs={'class': 'provincetr'}):
			for a in i.find_all('a'):
				link_id = re.sub("\D", "", a.get('href'))
				province_dict[link_id] = {'id': link_id, 'name': a.text, 'pid': '0', 'pid1': '0', 'pid2': '0', 'pid3': '0', 'pid4': '0',
				             'code': id}
				# time.sleep(1 / 10)
	return province_dict


def get_city (url, header, lists):
	# 获取省下级市
	l = lists.copy()
	for i in l:
		page_content = GetHttp(url + i + '.html', header).text
		if not page_content:
			continue
		soup = BeautifulSoup(page_content, 'html.parser')
		for v in soup.find_all(attrs={'class': 'citytr'}):
			id = str(v.find_all('td')[0].text)
			if id[0:4] not in lists.keys():
				lists[id[0:4]] = {'id': id[0:4], 'name': str(v.find_all('td')[1].text), 'pid': '0', 'pid1': i,
				                  'pid2': '0', 'pid3': '0', 'pid4': '0', 'code': id}
	return lists


def county_tr (u, he, lists):
	# 获取市下级县
	l = lists.copy()
	a = {}
	for i in l:
		t = GetHttp(u + i[0:2] + '/' + i + '.html', he, 'gbk').text
		if not t:
			continue
		soup = BeautifulSoup(t, 'html.parser')
		for v in soup.find_all(attrs={'class': 'countytr'}):
			id = str(v.find_all('td')[0].text)
			if id[0:6] not in lists.keys():
				lists[id[0:6]] = {'id': id[0:6], 'name': str(v.find_all('td')[1].text), 'pid': '0',
				                  'pid1': l[i]['pid1'], 'pid2': i, 'pid3': '0', 'pid4': '0', 'code': id}
	return lists


def town_tr (u, he, lists):
	# 县下级镇
	l = lists.copy()
	for i in l:
		t = GetHttp(u + i[0:2] + '/' + i[2:4] + '/' + i + '.html', he, 'gbk').text
		if not t:
			continue
		soup = BeautifulSoup(t, 'html.parser')
		for v in soup.find_all(attrs={'class': 'towntr'}):
			id = str(v.find_all('td')[0].text)
			if id[0:9] not in lists.keys():
				lists[id[0:9]] = {'id': id[0:9], 'name': str(v.find_all('td')[1].text), 'pid': '0',
				                  'pid1': l[i]['pid1'], 'pid2': l[i]['pid2'], 'pid3': i, 'pid4': '0', 'code': id}
	return lists


def village_tr (u, he, lists):
	# 镇下级村
	l = lists.copy()
	for i in l:
		t = GetHttp(u + i[0:2] + '/' + i[2:4] + '/' + i[4:6] + '/' + i + '.html', he, 'gbk').text
		if not t:
			continue
		soup = BeautifulSoup(t, 'html.parser')
		for v in soup.find_all(attrs={'class': 'villagetr'}):
			id = str(v.find_all('td')[0].text)
			if id[0:12] not in lists.keys():
				lists[id[0:12]] = {'id': id[0:12], 'name': str(v.find_all('td')[1].text), 'pid': '0',
				                   'pid1': l[i]['pid1'], 'pid2': l[i]['pid2'], 'pid3': l[i]['pid2'], 'pid4': i,
				                   'code': id}
	return lists

print('省')
province_dict = get_province(url=url, header=header)
print('市')
c = get_city(url=url, header=header, lists=p)
print('县')
o = county_tr(u=url, he=header, lists=c)
print('镇')
t = town_tr(u=url, he=header, lists=o)
print('村')
v = village_tr(u=url, he=header, lists=t)


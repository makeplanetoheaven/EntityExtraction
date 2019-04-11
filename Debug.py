# coding=utf-8

# 引入外部库


# 引入内部库
from EntityRelation.GeographicalDomain.China.CityCrawler import *


if __name__ == '__main__':
	result_dict = {}
	get_province(result_dict)
	get_city(result_dict)
	get_county(result_dict)
	get_town(result_dict)
	get_village(result_dict)
	format_conversion(result_dict)

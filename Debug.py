# coding=utf-8

# 引入外部库
import json
import gc

# 引入内部库
from EntityRelation.GeographicalDomain.China.CityCrawler import *
from EntityInformation.BaiduEncyclopedia import *


def cnc_entity_rel_extract ():
	# 实体关系抽取
	result_dict = {}
	get_province(result_dict)
	get_city(result_dict)
	get_county(result_dict)
	get_town(result_dict)
	get_village(result_dict)
	entity_info, entity_rel = format_conversion(result_dict)

	del result_dict
	gc.collect()

	with open('./CacheData/EntityInfo.json', 'w', encoding='utf-8') as file_object:
		json.dump(entity_info, file_object, ensure_ascii=False, indent=2)
	with open('./CacheData/EntityRel.json', 'w', encoding='utf-8') as file_object:
		json.dump(entity_rel, file_object, ensure_ascii=False, indent=2)

def cnc_entity_info_extract ():
	# 实体信息抽取
	with open('./CacheData/GeographicalDomain/China/City/EntityInfo.json', 'r', encoding='utf-8') as file_object:
		entity_info_list = json.load(file_object)

	entity_info_extract(entity_info_list[0]['property'])

if __name__ == '__main__':
	cnc_entity_info_extract()

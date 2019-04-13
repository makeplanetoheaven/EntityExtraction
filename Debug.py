# coding=utf-8

# 引入外部库
import json
import gc

# 引入内部库
from EntityRelation.GeographicalDomain.China.CityCrawler import *


if __name__ == '__main__':
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

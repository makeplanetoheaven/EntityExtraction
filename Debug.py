# coding=utf-8


# 引入外部库
import json
import gc

# 引入内部库
from EntityRelation.GeographicalDomain.China.CityCrawler import *
from EntityRelation.GeographicalDomain.China.AirportCrawler import *
from EntityInformation.BaiduEncyclopedia import *
from Neo4j.Neo4j import *


def cnc_entity_rel_extract () -> None:
	"""
	实体关系抽取
	:return: None
	"""
	result_dict = {}
	get_province(result_dict)
	get_city(result_dict)
	get_county(result_dict)
	get_town(result_dict)
	get_village(result_dict)
	entity_info, entity_rel = format_conversion(result_dict)

	del result_dict
	gc.collect()

	with open('./CacheData/GeographicalDomain/China/City/EntityInfo.json', 'w', encoding='utf-8') as file_object:
		json.dump(entity_info, file_object, ensure_ascii=False, indent=2)
	with open('./CacheData/GeographicalDomain/China/City/EntityInfo.json', 'w', encoding='utf-8') as file_object:
		json.dump(entity_rel, file_object, ensure_ascii=False, indent=2)


def cnc_entity_info_extract () -> None:
	"""
	实体信息抽取（无多义词）
	:return: None
	"""
	with open('./CacheData/GeographicalDomain/China/City/EntityInfo.json', 'r', encoding='utf-8') as file_object:
		entity_info_list = json.load(file_object)

	for entity_info in entity_info_list:
		entity_info_extract(entity_info['property'])

	with open('./CacheData/GeographicalDomain/China/City/EntityInfo.json', 'w', encoding='utf-8') as file_object:
		json.dump(entity_info_list, file_object, ensure_ascii=False, indent=2)


def cnc_save () -> None:
	with open('./conn_info.json', 'r', encoding='utf-8') as file_object:
		conn = json.load(file_object)
	with open('./CacheData/GeographicalDomain/China/City/EntityInfo.json', 'r', encoding='utf-8') as file_object:
		entity_info = json.load(file_object)
	with open('./CacheData/GeographicalDomain/China/City/EntityRel.json', 'r', encoding='utf-8') as file_object:
		entity_rel = json.load(file_object)

	neo4j = Neo4j(ip=conn['ip'], password=conn['password'])
	neo4j.crate_graph(entity_info, entity_rel)


def cna_entity_rel_extract () -> None:
	"""
	实体关系抽取
	:return: None
	"""
	result_dict = {}
	get_airport(result_dict)
	# entity_info, entity_rel = format_conversion(result_dict)

	del result_dict
	gc.collect()
    #
	# with open('./CacheData/GeographicalDomain/China/City/EntityInfo.json', 'w', encoding='utf-8') as file_object:
	# 	json.dump(entity_info, file_object, ensure_ascii=False, indent=2)
	# with open('./CacheData/GeographicalDomain/China/City/EntityInfo.json', 'w', encoding='utf-8') as file_object:
	# 	json.dump(entity_rel, file_object, ensure_ascii=False, indent=2)

if __name__ == '__main__':
	cna_entity_rel_extract()

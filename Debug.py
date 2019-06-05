# coding=utf-8


# 引入外部库
import json
import gc

# 引入内部库
from EntityRelation.GeographicalDomain.China.CityCrawler import *
from EntityRelation.GeographicalDomain.China.AirportCrawler import *
from EntityRelation.GeographicalDomain.China.TrainStationCrawler import *
from EntityRelation.GeographicalDomain.China.RegionCrawler import *
from EntityInformation.BaiduEncyclopedia import *
from Neo4j.Neo4j import *


def cnc_entity_extract () -> None:
	"""
	中国城市实体关系抽取
	:return: None
	"""
	result_dict = {}
	get_province(result_dict)
	get_city(result_dict)
	get_county(result_dict)
	get_town(result_dict)
	get_village(result_dict)
	entity_info_list, entity_rel = format_conversion(result_dict)

	del result_dict
	gc.collect()

	for entity_info in entity_info_list:
		entity_info_extract(entity_info['property'])

	with open('./CacheData/GeographicalDomain/China/City/EntityInfo.json', 'w', encoding='utf-8') as file_object:
		json.dump(entity_info_list, file_object, ensure_ascii=False, indent=2)
	with open('./CacheData/GeographicalDomain/China/City/EntityRel.json', 'w', encoding='utf-8') as file_object:
		json.dump(entity_rel, file_object, ensure_ascii=False, indent=2)


def cnc_save () -> None:
	with open('./conn_info.json', 'r', encoding='utf-8') as file_object:
		conn = json.load(file_object)
	with open('./CacheData/GeographicalDomain/China/City/EntityInfo.json', 'r', encoding='utf-8') as file_object:
		entity_info = json.load(file_object)
	with open('./CacheData/GeographicalDomain/China/City/EntityRel.json', 'r', encoding='utf-8') as file_object:
		entity_rel = json.load(file_object)

	neo4j = Neo4j(ip=conn['ip'], password=conn['password'])
	neo4j.crate_graph(entity_info, entity_rel)


def cna_entity_extract () -> None:
	"""
	中国机场实体信息及关系抽取
	:return: None
	"""
	entity_info_list, entity_rel = get_airport()
	for entity_info in entity_info_list:
		entity_info_extract(entity_info['property'])

	with open('./CacheData/GeographicalDomain/China/Airport/EntityInfo.json', 'w', encoding='utf-8') as file_object:
		json.dump(entity_info_list, file_object, ensure_ascii=False, indent=2)
	with open('./CacheData/GeographicalDomain/China/Airport/EntityRel.json', 'w', encoding='utf-8') as file_object:
		json.dump(entity_rel, file_object, ensure_ascii=False, indent=2)


def cna_save () -> None:
	with open('./conn_info.json', 'r', encoding='utf-8') as file_object:
		conn = json.load(file_object)
	with open('./CacheData/GeographicalDomain/China/Airport/EntityInfo.json', 'r', encoding='utf-8') as file_object:
		entity_info = json.load(file_object)
	with open('./CacheData/GeographicalDomain/China/Airport/EntityRel.json', 'r', encoding='utf-8') as file_object:
		entity_rel = json.load(file_object)

	neo4j = Neo4j(ip=conn['ip'], password=conn['password'])
	neo4j.add_graph(entity_info, entity_rel)


def cnt_entity_extract () -> None:
	"""
	中国火车站实体信息及关系抽取
	:return: None
	"""
	entity_info_list, entity_rel = get_train_station()
	for entity_info in entity_info_list:
		entity_info_extract(entity_info['property'])

	with open('./CacheData/GeographicalDomain/China/TrainStation/EntityInfo.json', 'w', encoding='utf-8') as file_object:
		json.dump(entity_info_list, file_object, ensure_ascii=False, indent=2)
	with open('./CacheData/GeographicalDomain/China/TrainStation/EntityRel.json', 'w', encoding='utf-8') as file_object:
		json.dump(entity_rel, file_object, ensure_ascii=False, indent=2)


def cnt_save () -> None:
	with open('./conn_info.json', 'r', encoding='utf-8') as file_object:
		conn = json.load(file_object)
	with open('./CacheData/GeographicalDomain/China/TrainStation/EntityInfo.json', 'r', encoding='utf-8') as file_object:
		entity_info = json.load(file_object)
	with open('./CacheData/GeographicalDomain/China/TrainStation/EntityRel.json', 'r', encoding='utf-8') as file_object:
		entity_rel = json.load(file_object)

	neo4j = Neo4j(ip=conn['ip'], password=conn['password'])
	neo4j.add_graph(entity_info, entity_rel)


def cnr_entity_extract () -> None:
	"""
	中国区域实体信息及关系抽取
	:return: None
	"""
	entity_info_list, entity_rel = get_region()
	for entity_info in entity_info_list:
		entity_info_extract(entity_info['property'])

	with open('./CacheData/GeographicalDomain/China/Region/EntityInfo.json', 'w', encoding='utf-8') as file_object:
		json.dump(entity_info_list, file_object, ensure_ascii=False, indent=2)
	with open('./CacheData/GeographicalDomain/China/Region/EntityRel.json', 'w', encoding='utf-8') as file_object:
		json.dump(entity_rel, file_object, ensure_ascii=False, indent=2)


def cnr_save () -> None:
	with open('./conn_info.json', 'r', encoding='utf-8') as file_object:
		conn = json.load(file_object)
	with open('./CacheData/GeographicalDomain/China/Region/EntityInfo.json', 'r', encoding='utf-8') as file_object:
		entity_info = json.load(file_object)
	with open('./CacheData/GeographicalDomain/China/Region/EntityRel.json', 'r', encoding='utf-8') as file_object:
		entity_rel = json.load(file_object)

	neo4j = Neo4j(ip=conn['ip'], password=conn['password'])
	neo4j.add_graph(entity_info, entity_rel)

if __name__ == '__main__':
	cna_save()
	cnt_save()
	cnr_save()

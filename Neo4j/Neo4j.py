# coding=utf-8

# 引入外部库
from py2neo import *
from tqdm import tqdm

# 引入内部库


class Neo4j:
	def __init__ (self, ip: str, password: str, user='neo4j', http_port=7474, https_port=7473, bolt_port=7687):
		# Neo4j数据库连接
		self.graph = Graph(host=ip, password=password, user=user, http_port=http_port, https_port=https_port,
		                   bolt_port=bolt_port)
		self.node_matcher = NodeMatcher(self.graph)

	def crate_graph (self, entity_info: list, entity_rel: list) -> None:
		"""
		根据所传入的实体信息链表和实体关系三元组链表，构建子图，并存储到Neo4j
		注意：不考虑图谱中已经存在的相同实体
		:param entity_info: element: {type: str, property: dict}
		:param entity_rel: element: (n1_index, {name: str, property: dict}, n2_index)
		:return: None
		"""
		nodes = {}
		index = 0

		print('开始创建实体节点！')
		for info in tqdm(entity_info):
			node = Node(info['type'], name=info['property']['name'])
			node.update(info['property'])
			nodes[index] = node
			self.graph.create(node)
			index += 1

		print('开始创建实体间关系！')
		for rel in tqdm(entity_rel):
			relation = Relationship(nodes[rel[0]], rel[1]['name'], nodes[rel[2]])
			relation.update(rel[1]['property'])
			self.graph.create(relation)

	def add_graph (self, entity_info: list, entity_rel: list) -> None:
		"""
		根据所传入的实体信息链表和实体关系三元组链表，
		在已有实体的基础上，增加新的实体，及实体间关系。
		注意：关系三元组中，实体类型为字符串的实体，在图数据库中可能存在
		:param entity_info: element: {type: str, property: dict}
		:param entity_rel: element: (n1_index/n1_str, {name: str, property: dict}, n2_index/n2_str)
		:return: None
		"""
		nodes = {}
		index = 0

		print('开始创建新的实体节点！')
		for info in tqdm(entity_info):
			node = Node(info['type'], name=info['property']['name'])
			node.update(info['property'])
			nodes[index] = node
			self.graph.create(node)
			index += 1

		print('开始创建已有实体和新实体间关系！')
		for rel in tqdm(entity_rel):
			# 判断实体1类型
			if isinstance(rel[0], str):
				node1 = self.node_matcher.match(name=rel[0]).first()
			else:
				node1 = nodes[rel[0]]

			# 判断实体2类型
			if isinstance(rel[2], str):
				node2 = self.node_matcher.match(name=rel[2]).first()
			else:
				node2 = nodes[rel[2]]

			# 创建实体关系对象
			if node1 is not None and node2 is not None:
				relation = Relationship(node1, rel[1]['name'], node2)
				relation.update(rel[1]['property'])
				self.graph.create(relation)

	def update_graph (self):
		pass

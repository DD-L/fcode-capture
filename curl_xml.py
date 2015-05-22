#! /usr/bin/python
#encoding=utf-8

from  xml.dom import  minidom

class CaptureInstance:
	__instance = {}
	__instance_id = ''
	__instance_name = ''
	__instance_curl = ''
	__instance_regex = ''
	__instance_interval = 30
	__instance_callback = ''
	__xmlfile = ''

	def __init__(self, xmlfile = 'curl.xml'):
		self.__xmlfile = xmlfile
		self.__instance_interval = 30

	def __get_attrvalue(self, node, attrname):
		return node.getAttribute(attrname) if node else ''

	def __get_nodevalue(self, node, index = 0):
		return node.childNodes[index].nodeValue if node else ''

	def __get_xmlnode(self, node, name):
		return node.getElementsByTagName(name) if node else []

	# 基于id, 得到一个 instance 对象
	def get_instance_data(self, ins_id):
		doc = minidom.parse(self.__xmlfile) 
		root = doc.documentElement
		instance_nodes = self.__get_xmlnode(root, 'instance')
		for node in instance_nodes: 
			self.__instance_id = self.__get_attrvalue(node, 'id')
			if ins_id != self.__instance_id:
				continue;
			node_name = self.__get_xmlnode(node, 'name')
			node_curl = self.__get_xmlnode(node, 'curl')
			node_regex = self.__get_xmlnode(node, 'regex')
			node_interval = self.__get_xmlnode(node, 'interval')
			node_callback = self.__get_xmlnode(node, 'callback')

			self.__instance_name = self.__get_nodevalue(node_name[0]).encode('utf-8', 'ignore').strip()
			self.__instance_curl = self.__get_nodevalue(node_curl[0]).encode('utf-8', 'ignore').strip()
			self.__instance_regex = self.__get_nodevalue(node_regex[0]).encode('utf-8', 'ignore').strip()
			# 处理默认节点 interval
			if node_interval:
				interval = int(self.__get_nodevalue(node_interval[0]).encode('utf-8', 'ignore').strip()) 
				if interval >= 0:
					self.__instance_interval = interval
			self.__instance_callback = self.__get_nodevalue(node_callback[0]).encode('utf-8', 'ignore').strip()

			self.__instance['id'] , self.__instance['name'] , self.__instance['curl'] ,\
			self.__instance['regex'] , self.__instance['interval'], self.__instance['callback'] = (
				self.__instance_id, self.__instance_name, self.__instance_curl,\
				self.__instance_regex , int(self.__instance_interval), self.__instance_callback
			)
			return self.__instance
		return {} 
	
	# 输出xml 文本
	def xml_to_string(self):
		doc = minidom.parse(self.__xmlfile)
		return doc.toxml('UTF-8')

#def test_load_xml(filename):
#    instance_list = get_xml_data(filename)
#    for instance in instance_list :
#        print '-----------------------------------------------------'
#        if instance:
#			print 'id: ' + str(instance['id'])
#			print 'name: ' + instance['name']
#			print 'curl: ' + instance['curl']
#			print 'regex: ' + instance['regex']
#			print 'interval:' + str(instance['interval'])
#			print '=================================================='

#if __name__ == "__main__":
#	ci = CaptureInstance()
#	ret = ci.get_instance_data(3)
#	if ret:
#		print ret
#	else:
#		print 'No' 
	

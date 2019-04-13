# coding=utf-8

# 引入外部库
import requests
import random
import time


# 引入内部库


class GetHttp:
	def __init__ (self, wait_time=15):
		# 存储user agent
		self.user_agent_list = [
			"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
			"Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
			"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
			"Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
			"Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
			"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
			"Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
			"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
			"Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
			"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
			"Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
			"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
			"Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
			"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
			"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
			"Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
			"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
			"Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"]

		# 代理IP
		self.ip_list = ['http://112.87.71.154:8090',
		                'http://110.52.235.53:9999',
		                'http://223.241.116.121:8010',
		                'http://183.148.148.189:9999']

		# 等待时间
		self.wait_time = wait_time

	def get_page_content (self, url: str, timeout: int, proxy=None, num_retries=6, charset='gbk')->str:
		"""
		通过指定url地址获取网页内容
		:param url: 网址
		:param timeout: 超时时间设置
		:param proxy: 代理
		:param num_retries: 重试次数
		:param charset: 编码格式
		:return: 爬取到的网页内容
		"""
		# 从user_agent_list中随机抽取出一个字符串
		ua = random.choice(self.user_agent_list)

		# 构造一个完整的User_Agent
		header = {"User-Agent": ua}

		# 当代理为空时，不使用代理获取response
		if proxy is None:
			try:
				response = requests.get(url, headers=header, timeout=timeout)
				response.encoding = charset
				return response.text
			except:
				if num_retries > 0:
					time.sleep(self.wait_time)
					print(u"获取网页错误，"+str(self.wait_time)+"s后将获取倒数第：", num_retries, u"次")
					# 调用自身并将次数减1
					return self.get_page_content(url, timeout, num_retries=num_retries - 1)
				else:
					print(u"开始使用代理")
					time.sleep(self.wait_time)
					IP = "".join(str(random.choice(self.ip_list)).strip())
					proxy = {"http": IP}
					return self.get_page_content(url, timeout, proxy)
		else:
			try:
				# 随机取IP并去除空格
				IP = "".join(str(random.choice(self.ip_list)).strip())
				# 构造一个代理
				proxy = {"http": IP}
				# 使用代理来获取response
				response = requests.get(url, headers=header, proxies=proxy, timeout=timeout)
				response.encoding = charset
				return response.text
			except:
				if num_retries > 0:
					time.sleep(self.wait_time)
					IP = "".join(str(random.choice(self.ip_list)).strip())
					print(u"正在更换代理，"+str(self.wait_time)+"s后将重新获取第", num_retries, u"次")
					print(u"当前代理是：", proxy)
					return self.get_page_content(url, timeout, proxy, num_retries - 1)
				else:
					print(u"代理发生错误，取消代理")
					return self.get_page_content(url, 3)

		pass

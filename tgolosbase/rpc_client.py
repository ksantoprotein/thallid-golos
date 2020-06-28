# -*- coding: utf-8 -*-

from requests import Session
from requests.adapters import HTTPAdapter
from requests.exceptions import ConnectionError

import json
from time import sleep, time
from pprint import pprint
from itertools import cycle

from .storage import nodes, api_total
from .proxy import Proxy

class Http():

	http = Session()
	proxies = None


class RpcClient(Http):

	RPS_DELAY = 1.00	# ~3 requests per second
	last_request = 0.0
	
	""" Simple Steem JSON-RPC API
		This class serves as an abstraction layer for easy use of the Steem API.

		rpc = RpcClient(nodes=nodes) or rpc = RpcClient()
		Args:
			nodes (list): A list of Steem HTTP RPC nodes to connect to.
		
		any call available to that port can be issued using the instance
		rpc.call('command', *parameters)
	"""
	
	headers = {'User-Agent': 'thallid', 'content-type': 'application/json'}

	
	def __init__(self, report=False, **kwargs):

		self.api_total = api_total
		
		self.report = report
		self.PROXY = kwargs.get("PROXY", False)
		if self.PROXY: self.proxies = Proxy()

		self.nodes = cycle(kwargs.get("nodes", nodes))		# Перебор нод
		self.url = next(self.nodes)
		
		self.num_retries = kwargs.get("num_retries", 3)		# Количество попыток подключения к ноде
		adapter = HTTPAdapter(max_retries=self.num_retries)
		for node in nodes:
			self.http.mount(node, adapter)
			
		
	def get_response(self, payload):
	
		data = json.dumps(payload, ensure_ascii=False).encode('utf8')
	
		while True:
				
			n = 1
			proxies = self.proxies.get_http() if self.PROXY else None
			while n < self.num_retries:
				try:
				
					# Ограничение по запросам в секунду
					delay = self.RPS_DELAY - (time() - self.last_request)
					if delay > 0: sleep(delay)
				
					#response = self.http.post(self.url, data=data, headers=self.headers, proxies=proxies, auth=auth)
					response = self.http.post(self.url, data=data, headers=self.headers, proxies=proxies, timeout=30)
					self.last_request = time()
					
					if response.status_code == 503:
						proxies = self.proxies.new_http() if self.PROXY else None	# next proxy
						print('new proxy', proxies)
					else:
						return response
					
				#except ConnectionError as ce:
				except:
					#print('ce', ce)
					sleeptime = (n - 1) * 2
					if self.report:
						print("Lost connection to node during rpcconnect(): %s (%d/%d) " % (self.url, n, self.num_retries))
						print("Retrying in %d seconds" % sleeptime)
					sleep(sleeptime)
					n += 1
					
			self.url = next(self.nodes)			# next node
			print("Trying to connect to node %s" % self.url, 'error in get_response rpc_client', proxies)
				
		return False

					
	def call(self, name, *params, **kwargs):
	
		# Определяем для name своё api
		api = self.api_total[name]
		#method = kwargs.get('method', 'condenser_api.')	#steem
		method = kwargs.get('method', 'call')
		parameters = kwargs.get('params', [api, name, params])
		#payload = {"method": method + name, "params": parameters, "id": 1, "jsonrpc": '2.0'}	#steem
		payload = {"method": method, "params": parameters, "id": 1, "jsonrpc": '2.0'}
		result = None
		
		n = 1
		while n < self.num_retries:
			response = self.get_response(payload)

			if response:
				if response.status_code == 200:
					try:
						res = response.json()
						if 'error' in res:
							if self.report:
								#pprint(res["error"]["message"])
								print('ERROR IN RES', res["error"]["message"])
						else:
							result = res["result"]
							break
					except:
						print('ERROR JSON', response)
				#elif response.status_code == 503:
				#	proxies = self.proxies.new_http() if self.PROXY else None	# next proxy
				#	print('new proxy', proxies)

				else:
					if self.report:
						print(n, 'ERROR status_code', response.status_code, response.text)
			else:
				print('not connection to node', self.url)
				
			print('response', response)
			n += 1
			self.url = next(self.nodes)			# next node
			sleep(n * 2)
			print("Trying to connect to node %s" % self.url, 'for method', name)
		
		return result


#----- main -----
if __name__ == '__main__':
	pass
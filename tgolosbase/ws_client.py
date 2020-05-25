# -*- coding: utf-8 -*-

import websocket
import ssl
import json
from .storage import nodes, api_total
from time import sleep
from pprint import pprint
from itertools import cycle


class WsClient():

	""" Simple Golos JSON-WebSocket-RPC API
		This class serves as an abstraction layer for easy use of the Golos API.

		rpc = WsClient(nodes = nodes) or rpc = WsClient()
		Args:
			nodes (list): A list of Golos WebSocket RPC nodes to connect to.
		
		any call available to that port can be issued using the instance
		rpc.call('command', *parameters)
	"""
	
	def __init__(self, report=False, **kwargs):

		self.report = report
		self.num_retries = kwargs.get("num_retries", 20)
		self.nodes = cycle(kwargs.get("nodes", nodes))	# Перебор нод
		self.api_total = api_total
		self.url = ''
		self.ws = None
		self.ws_connect()												# Подключение к ноде

		
	def ws_connect(self):
		cnt = 0
		while True:
			cnt += 1
			self.url = next(self.nodes)
			if self.report:
				print("Trying to connect to node %s" % self.url)
			if self.url[:3] == "wss":
				sslopt_ca_certs = {'cert_reqs': ssl.CERT_NONE}
				self.ws = websocket.WebSocket(sslopt=sslopt_ca_certs)
			else:
				self.ws = websocket.WebSocket()

			try:
				self.ws.connect(self.url)
				break
			except KeyboardInterrupt:
				raise
			except:
				if self.num_retries >= 0 and cnt > self.num_retries:
					raise Exception	###

				sleeptime = (cnt - 1) * 2 if cnt < 10 else 10
				if sleeptime:
					if self.report:
						print("Lost connection to node during wsconnect(): %s (%d/%d) " % (self.url, cnt, self.num_retries))
						print("Retrying in %d seconds" % sleeptime)
					sleep(sleeptime)

					
	def call(self, name, *args):
	
		# Определяем для name своё api
		api = self.api_total[name]
		if api:
			body_dict = {"id": 1, "method": "call", "jsonrpc": "2.0", "params": [api, name, args]}
			body = json.dumps(body_dict, ensure_ascii = False).encode('utf8')
		else:
			if self.report:
				print('not find api in api_total')
			return False
		
		response, result = None, []

		cnt = 0
		while True:
			cnt += 1

			try:
				self.ws.send(body)
				response = self.ws.recv()
				#pprint(response)
				break
			except KeyboardInterrupt:
				raise
			except:
				if self.num_retries > -1 and cnt > self.num_retries:
					raise Exception	### возможно сделать return False
				sleeptime = (cnt - 1) * 2 if cnt < 10 else 10
				if sleeptime:
					if self.report:
						print("Lost connection to node during call(): %s (%d/%d) " % (self.url, cnt, self.num_retries))
						print("Retrying in %d seconds" % sleeptime)
					sleep(sleeptime)

				# retry
				try:
					self.ws.close()
					sleep(sleeptime)
					self.ws_connect()
				except:
					pass

		if response:
			response_json = json.loads(response)	# Нет проверки на ошибки при загрузке данных
		else:
			if self.report:
				print('not response')
			return False
			
		if 'error' in response_json:
			if self.report:
				print('find error')
				print(response_json["error"]["message"])
				#pprint(response_json)
			return False
		elif 'result' in response_json:
			result = response_json.get("result")
			#if 'broadcast' in name:
			#	pprint(result)
			
		else:
			if self.report:
				print('not result')
				#pprint(response_json)
				#print(response_json["message"])
			return False
				
		return(result)


#----- main -----
if __name__ == '__main__':

	print('connect')
	rpc = WsClient()
	print('try call')

	i = rpc.call('get_dynamic_global_properties')
	#i = rpc.call('get_accounts', ['koss'])
	#i = rpc.call('get_block', '20005000')
	pprint(i)

	print('yet')
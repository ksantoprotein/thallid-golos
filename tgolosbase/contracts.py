# -*- coding: utf-8 -*-

from pprint import pprint
import json
from time import sleep, time
from random import randint
from datetime import datetime, timedelta

#UInt32 - [ 0 : 4294967295 ]


class TGolosMomsters():

	bot = 'azino777'
	contract = 'tgm'
	sets = {
			"alpha": ['pioner', 'vlad', 'varwar', 'blackmoon', 'dash', 'kartmen', 'anton'],
			}
	level = {
			"alpha": [str(i) for i in range(1, 10)],
			}
	
	def __init__(self, b4, **kwargs):

		self.b4 = b4
		print('append smart contract Thallid Golos Monsters')
		
	##### ##### SMART ##### #####
	
	def emission(self, name, set, seed, from_account, wif, **kwargs):
	
		player = kwargs.get("player", from_account)
		contract = {
					"contract": self.contract,
					"action": "emission",
					"payload": {
								"card": name,
								"set": set,
								"seed": seed,
								"player": player,
								},
					}
		memo = json.dumps(contract)
		
		return(self.b4.transfer('null', 0.001, 'GBG', from_account, wif, memo = memo))
		
	##### ##### CHECK ##### #####
		
	def check(self, op):
	
		amount, asset = self.resolve_amount(op["amount"])
		account = op["from"]
		to = op["to"]
		memo = op["memo"]
		memo = ' '.join(memo.split())		# Удаление лишних пробелов впереди и сзади, удаление табуляции и неразрывных пробелов
		
		if (memo[0] == '{') and (memo[-1] == '}') and (self.contract in memo):		# contract {} and 'tgm'
			try:
				contract = json.loads(memo)
			except:
				try:
					contract = json.loads(unicodedata.normalize("NFKD", memo))
				except:
					print('error format contract', amount, account, memo)	### в файл бы записать подобные ошибки с номерами блоков и прочего
					return({"error": True, "message": 'error format contract'})
				
			contractName = contract.get("contract", None)
			contractAction = contract.get("action", None)
			contractPayload = contract.get("payload", None)
			
			if None in [contractName, contractAction, contractPayload]:
				return({"error": True, "message": 'error values contract'})
				
			if contractName == self.contract:		### Контракт данной ветки tgm
			
				if contractAction == 'emission':	# Выпуск новой карты
					return(self.check_emission(contractPayload))
			
		return False
		
				
	def check_emission(self, payload):
				
		card = payload.get("card", None)
		set = payload.get("set", None)
		seed = payload.get("seed", None)
		player = payload.get("player", None)
	
		if None in [card, set, seed, player]:
			return({"error": True, "message": 'error values card'})
			
		if not self.b4.is_login(player):
			return({"error": True, "message": 'error login player'})
		if set not in self.sets:
			return({"error": True, "message": 'error set'})
		if card not in self.sets[set]:
			return({"error": True, "message": 'error name card'})
		try:
			if (0 > seed > 4294967295):
				return({"error": True, "message": 'error value seed'})
		except:
			return({"error": True, "message": 'error type seed'})

		# Get level card
		k1, k2 = self.b4.key.get_sm_keys(card, set, str(seed))
		list1, list2 = list(k1), list(k2)
		maska = [list1[n] for n in range(50) if list1[n] == list2[n]]
		level = ''.join(sorted(maska)) if maska != [] else None
		if not level:
			return({"error": True, "message": 'error level card'})
		elif level not in self.level[set]:
			return({"error": True, "message": 'error value level card'})
			
		uid = '-'.join([card, set, str(seed)])
		mining = self.b4.get_content(self.bot + '/' + uid)
		author = mining["author"] if mining else ''
		if author == self.bot:
			print('mining')
			return({"error": True, "message": 'error mining yet card'})
			
		todo = ['emission', {"player": player, "card": card, "set": set, "seed": seed, "level": level}]
		return({"error": False, "contract": todo})
		
	def resolve_amount(self, am):
		amount, asset = am.split()
		return([float(amount), asset])
		
#########################################################################################
		
class Contract():

	def __init__(self, b4, **kwargs):

		self.b4 = b4
		
	##### ##### SMART ##### #####
	
	def emission(self, amount, asset, from_account, wif):
	
		contract = {
					"contractName": "tokens",
					"contractAction": "emission",
					"contractPayload": {
										"symbol": asset,
										},
					}
		memo = json.dumps(contract)
		
		return(self.b4.transfer('null', amount, 'GBG', from_account, wif, memo = memo))
		

	def transfer(self, to, amount, asset, from_account, wif, **kwargs):
	
		contract = {
					"contractName": "tokens",
					"contractAction": "transfer",
					"contractPayload": {
										"symbol": asset,
										"to": to,
										"quantity": amount,
										},
					}
					
		memo_contract = kwargs.get("memo", None)
		if memo:
			contract["contractPayload"]["memo"] = json.dumps(memo_contract),
					
		memo = json.dumps(contract)
		
		return(self.b4.transfer('null', 0.001, 'GBG', from_account, wif, memo = memo))
		
	##### ##### ##### ##### #####
	
	def resolve_amount(self, am):
		amount, asset = am.split()
		return([float(amount), asset])
		
	def check_asset(self, asset):
		if not asset:
			return False
		if 3 < len(asset) > 5:
			return False
		for l in list(asset):
			if l not in list('ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
				return False
		return True
	
		
	def check(self, op):
	
		amount, asset = self.resolve_amount(op["amount"])
		account = op["from"]
		to = op["to"]
		memo = op["memo"]
		
		if memo[0] == '{' and memo[-1] == '}':		# contract {}
			memo = ' '.join(memo.split())		
			try:
				contract = json.loads(memo)
			except:
				try:
					contract = json.loads(unicodedata.normalize("NFKD", memo))
				except:
					print('error format contract', amount, account, memo)	### в файл бы записать подобные ошибки с номерами блоков и прочего
					return False
				
			contractName = contract.get("contractName", None)
			contractAction = contract.get("contractAction", None)
			contractPayload = contract.get("contractPayload", None)
			
			if None in [contractName, contractAction, contractPayload]:
				return False
				
			if contractName == 'tokens':
			
				if contractAction == 'emission':
					if self.check_asset(contractPayload.get("symbol", None)):
						fee = int(amount * 1000)
						todo = [contractName, {contractAction: {"account": account, "asset": contractPayload["symbol"], "fee": fee}}]
						return todo
						
				elif contractAction == 'transfer':
					symbol = contractPayload.get("symbol", None)
					to = contractPayload.get("to", None)
					quantity = contractPayload.get("quantity", None)
					if None in [symbol, to, quantity]:
						return False
				
					if self.check_asset(symbol):
						try:
							fee = int(float(quantity) * 1000)
						except:
							print('error amount', quantity)
							return False
						
						if fee <= 0:
							print('error amount <=0', quantity)
							return False
							
						todo = [contractName, {contractAction: {"from_account": account, "to_account": to, "asset": symbol, "fee": fee}}]
						return todo

				
			pprint(contract)
			
		return False
		
		
	##### ##### THALLID ##### #####
	
	def buy_thl(self, amount, from_account, wif):
	
		contract = {
					"contractName": "thallid",
					"contractAction": "buy",
					"contractPayload": {
										"symbol": 'THL',
										},
					}
		memo = json.dumps(contract)
		
		return(self.b4.transfer('thallid', amount, 'GOLOS', from_account, wif, memo = memo))
		
	def sell_thl(self, amount, from_account, wif):
	
		thallid_contract = {
							"id": "thallid",
							"action": "sell",
							#"payload": {
							#			"symbol": 'THL',
							#			},
							}
		contract = {
					"contractName": "tokens",
					"contractAction": "transfer",
					"contractPayload": {
										"symbol": 'THL',
										"to": 'thallid',
										"quantity": amount,
										"memo": json.dumps(thallid_contract),
										},
					}
		memo = json.dumps(contract)
		
		return(self.b4.transfer('null', 0.001, 'GBG', from_account, wif, memo = memo))
		
	##### ##### ##### ##### #####
		
		
if __name__ == '__main__':
	print('test')
	from random import randint
	from tgolosbase.api import Api
	b4 = Api()
	tgm = TGolosMomsters(b4)
	
	player = 'ksantoprotein'
	set = 'alpha'
	
	n = 0
	while True:
		seed = randint(0, 4294967295)
		n += 1
		for card in tgm.sets["alpha"]:
			contract = {
						"contract": 'tgm',
						"action": 'emission',
						"payload": {"card": card, "set": set, "seed": seed, "player": player}
						}
			op = {
					"amount": '0.001 GBG',
					"from": 'ksantoprotein',
					"to": 'null',
					"memo": json.dumps(contract),
					}
			tx = tgm.check(op)
			if tx:
				if not tx["error"]:
					print(n, tx["contract"])
	
	input('END')
	
		
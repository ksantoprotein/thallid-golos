# -*- coding: utf-8 -*-

from pprint import pprint
import json

import hashlib
from binascii import hexlify, unhexlify
import ecdsa
from .base58 import gphBase58CheckEncode, base58CheckEncode, base58CheckDecode, gphBase58CheckDecode

from .storage import prefix

	
class Key():

	def __init__(self):
		self.roles = ["posting", "active", "memo", "owner"]
		self.prefix = prefix
		

	def get_keys(self, account, password):

		keys = {"login": account, "password": password, "private": {}, "public": {}}
		
		for role in self.roles:

			b = bytes(account + role + password, 'utf8')
			secret = hashlib.sha256(b).digest()					# bytes(b58)
			
			keys["private"][role] = self.get_private_from_secret(secret)
			keys["public"][role] = self.get_public_from_secret(secret)

			# base58CheckDecode(private_key)						# repr(b58) Gives the hex representation of the Graphene private key.
			# gphBase58CheckDecode(public_key[len(self.prefix):])	# repr(b58) Gives the hex representation of the Graphene public key.
			
			### Для игр
			#print(int(base58CheckDecode(private_key), 16))							# =>repr=>int 
			#print(int(gphBase58CheckDecode(public_key[len(self.prefix):]), 16))	# =>repr=>int 
			
			print(role, self.get_public_from_private(keys["private"][role]))
			
			print(self.is_key(keys["private"][role], keys["public"][role]))
			
		return(keys)
		
		
	##### ##### ##### ##### #####
	
	def get_private_from_secret(self, secret):
		k = hexlify(secret).decode('ascii')					# repr(b58) Gives the hex representation of the Graphene private key.
		private_key = base58CheckEncode(0x80, k)
		return(str(private_key))

	def get_public_from_secret(self, secret):
		order = ecdsa.SigningKey.from_string(secret, curve = ecdsa.SECP256k1).curve.generator.order()
		point = ecdsa.SigningKey.from_string(secret, curve = ecdsa.SECP256k1).verifying_key.pubkey.point
		x_str = ecdsa.util.number_to_string(point.x(), order)
		compressed = hexlify(chr(2 + (point.y() & 1)).encode("ascii") + x_str).decode("ascii")
		public_key = self.prefix + gphBase58CheckEncode(compressed)
		return(str(public_key))
		
	def get_public_from_private(self, wif):
		secret = unhexlify(base58CheckDecode(str(wif))) 	# Преобразование из приватного ключа
		public_key = self.get_public_from_secret(secret)
		return(str(public_key))
		
	def is_key(self, wif, public):
		res = True if public == self.get_public_from_private(wif) else False
		return res
		
	##### ##### ##### ##### #####

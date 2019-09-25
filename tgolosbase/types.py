import json
import struct
import time
from binascii import hexlify, unhexlify
from calendar import timegm

from .storage import asset_precision, prefix
from .base58 import Base58
from pprint import pprint


object_type = {
	"dynamic_global_property": 0,
	"reserved0": 1,
	"account": 2,
	"witness": 3,
	"transaction": 4,
	"block_summary": 5,
	"chain_property": 6,
	"witness_schedule": 7,
	"comment": 8,
	"category": 9,
	"comment_vote": 10,
	"vote": 11,
	"witness_vote": 12,
	"limit_order": 13,
	"feed_history": 14,
	"convert_request": 15,
	"liquidity_reward_balance": 16,
	"operation": 17,
	"account_history": 18,
}

timeformat = '%Y-%m-%dT%H:%M:%S%Z'


def varint(n):	#ok
	""" Varint encoding
	"""
	data = b''
	while n >= 0x80:
		data += bytes([(n & 0x7f) | 0x80])
		n >>= 7
	data += bytes([n])
	return data


def varintdecode(data):
	""" Varint decoding
	"""
	shift = 0
	result = 0
	for c in data:
		b = ord(c)
		result |= ((b & 0x7f) << shift)
		if not (b & 0x80):
			break
		shift += 7
	return result


def variable_buffer(s):
	""" Encode variable length buffer
	"""
	return varint(len(s)) + s


def JsonObj(data):
	""" Returns json object from data
	"""
	try:
		return json.loads(str(data))
	except:
		try:
			return data.__str__()
		except:
			raise ValueError('JsonObj could not parse %s:\n%s' %
							 (type(data).__name__, data.__class__))


class String:	### ok
	def __init__(self, d):
		self.data = d

	def __bytes__(self):
		d = self.unicodify()
		return varint(len(d)) + d

	def __str__(self):
		return '%s' % str(self.data)

	def unicodify(self):
		r = []
		for s in self.data:
			o = ord(s)
			if o <= 7:
				r.append("u%04x" % o)
			elif o == 8:
				r.append("b")
			elif o == 9:
				r.append("\t")
			elif o == 10:
				r.append("\n")
			elif o == 11:
				r.append("u%04x" % o)
			elif o == 12:
				r.append("f")
			elif o == 13:
				r.append("\r")
			elif 13 < o < 32:
				r.append("u%04x" % o)
			else:
				r.append(s)
		return bytes("".join(r), "utf-8")



							 
class Uint8:
	def __init__(self, d):
		self.data = d

	def __bytes__(self):
		return struct.pack("<B", self.data)

	def __str__(self):
		return '%d' % self.data


class Int16:	#ok
	def __init__(self, d):
		self.data = int(d)

	def __bytes__(self):
		return struct.pack("<h", int(self.data))

	def __str__(self):
		return '%d' % self.data


class Uint16:	#ok
	def __init__(self, d):
		self.data = int(d)

	def __bytes__(self):
		return struct.pack("<H", self.data)

	def __str__(self):
		return '%d' % self.data


class Uint32:
	def __init__(self, d):
		self.data = int(d)

	def __bytes__(self):
		return struct.pack("<I", self.data)

	def __str__(self):
		return '%d' % self.data


class Uint64:
	def __init__(self, d):
		self.data = int(d)

	def __bytes__(self):
		return struct.pack("<Q", self.data)

	def __str__(self):
		return '%d' % self.data


class Varint32:
	def __init__(self, d):
		self.data = d

	def __bytes__(self):
		return varint(self.data)

	def __str__(self):
		return '%d' % self.data


class Int64:
	def __init__(self, d):
		self.data = d

	def __bytes__(self):
		return struct.pack("<q", self.data)

	def __str__(self):
		return '%d' % self.data



class Bytes:
	def __init__(self, d, length=None):
		self.data = d
		if length:
			self.length = length
		else:
			self.length = len(self.data)

	def __bytes__(self):
		# FIXME constraint data to self.length
		d = unhexlify(bytes(self.data, 'utf-8'))
		return varint(len(d)) + d

	def __str__(self):
		return str(self.data)


class Void:
	def __init__(self):
		pass

	def __bytes__(self):
		return b''

	def __str__(self):
		return ""


class Array:
	def __init__(self, d):
		self.data = d
		self.length = Varint32(len(self.data))

	def __bytes__(self):
		return bytes(self.length) + b"".join([bytes(a) for a in self.data])

	def __str__(self):
		r = []
		for a in self.data:
			if isinstance(a, ObjectId):
				r.append(str(a))
			elif isinstance(a, VoteId):
				r.append(str(a))
			elif isinstance(a, String):
				r.append(str(a))
			else:
				r.append(JsonObj(a))
		return json.dumps(r)


class PointInTime:
	def __init__(self, d):
		self.data = d

	def __bytes__(self):
		return struct.pack("<I", timegm(time.strptime((self.data + "UTC"), timeformat)))

	def __str__(self):
		return self.data


class Signature:
	def __init__(self, d):
		self.data = d

	def __bytes__(self):
		return self.data

	def __str__(self):
		return json.dumps(hexlify(self.data).decode('ascii'))


class Bool(Uint8): # Bool = Uint8 #ok
	def __init__(self, d):
		super().__init__(d)

	def __str__(self):
		return True if self.data else False


class Set(Array): # Set = Array
	def __init__(self, d):
		super().__init__(d)


class FixedArray:
	def __init__(self, d):
		raise NotImplementedError

	def __bytes__(self):
		raise NotImplementedError

	def __str__(self):
		raise NotImplementedError


class Optional:	#ok
	def __init__(self, d):
		self.data = d

	def __bytes__(self):
		if not self.data:
			return bytes(Bool(0))
		else:
			return bytes(Bool(1)) + bytes(self.data) if bytes(self.data) else bytes(Bool(0))

	def __str__(self):
		return str(self.data)

	def isempty(self):
		if not self.data:
			return True
		return not bool(bytes(self.data))


class StaticVariant:
	def __init__(self, d, type_id):
		self.data = d
		self.type_id = type_id

	def __bytes__(self):
		return varint(self.type_id) + bytes(self.data)

	def __str__(self):
		return json.dumps([self.type_id, self.data.json()])


class Map:
	def __init__(self, data):
		self.data = data

	def __bytes__(self):
		b = b""
		b += varint(len(self.data))
		for e in self.data:
			b += bytes(e[0]) + bytes(e[1])
		return b

	def __str__(self):
		r = []
		for e in self.data:
			r.append([str(e[0]), str(e[1])])
		return json.dumps(r)


class Id:
	def __init__(self, d):
		self.data = Varint32(d)

	def __bytes__(self):
		return bytes(self.data)

	def __str__(self):
		return str(self.data)


class VoteId:
	def __init__(self, vote):
		parts = vote.split(":")
		assert len(parts) == 2
		self.type = int(parts[0])
		self.instance = int(parts[1])

	def __bytes__(self):
		binary = (self.type & 0xff) | (self.instance << 8)
		return struct.pack("<I", binary)

	def __str__(self):
		return "%d:%d" % (self.type, self.instance)


class ObjectId:
	""" Encodes object/protocol ids
	"""

	def __init__(self, object_str, type_verify=None):
		if len(object_str.split(".")) == 3:
			space, type, id = object_str.split(".")
			self.space = int(space)
			self.type = int(type)
			self.instance = Id(int(id))
			self.Id = object_str
			if type_verify:
				assert object_type[type_verify] == int(type), \
					"Object id does not match object type! " + \
					"Excpected %d, got %d" % \
					(object_type[type_verify], int(type))
		else:
			raise Exception("Object id is invalid")

	def __bytes__(self):
		return bytes(self.instance) # only yield instance

	def __str__(self):
		return self.Id
		

class Amount:	#ok
	def __init__(self, d):
		self.amount, self.asset = d.strip().split(" ")
		self.amount = float(self.amount)

		if self.asset in asset_precision:
			self.precision = asset_precision[self.asset]
		else:
			raise Exception("Asset unknown")

	def __bytes__(self):
		# padding
		asset = self.asset + "\x00" * (7 - len(self.asset))
		amount = round(float(self.amount) * 10 ** self.precision)
		return (
				struct.pack("<q", amount) +
				struct.pack("<b", self.precision) +
				bytes(asset, "ascii")
		)

	def __str__(self):
		return '{:.{}f} {}'.format(
			self.amount,
			self.precision,
			self.asset
		)

		
class Beneficiaries:

	def __init__(self, d):
		self.data = d

	def __bytes__(self):
		b = varint(len(self.data))
		for beneficiary in self.data:
			b += bytes(String(beneficiary["account"]))
			b += bytes(Uint16(beneficiary["weight"]))
		return b

	def __str__(self):
		return str(self.data)


class PublicKey:	#ok

	def __init__(self, d):
		self.data = d

	def __bytes__(self):
		return bytes(Base58(self.data, prefix = prefix))

	def __str__(self):
		return str(self.data)


class Permission:	#ok

	def __init__(self, d):
		self.data = d

	def __bytes__(self):
	
		b = bytes(Uint32(self.data["weight_threshold"]))
		
		b += varint(len(self.data["account_auths"]))			# Array []
		for account, weight in self.data["account_auths"]:
			b += bytes(String(account))
			b += bytes(Uint16(weight))
			
		b += varint(len(self.data["key_auths"]))				# Array []
		for key, weight in self.data["key_auths"]:
			b += bytes(PublicKey(key))
			b += bytes(Uint16(weight))
	
		return b

	def __str__(self):
		return str(self.data)
		

class Optional_Permission:	#ok
	def __init__(self, d):
		self.data = Permission(d) if d else d

	def __bytes__(self):
		if not self.data:
			return bytes(Bool(0))
		else:
			return bytes(Bool(1)) + bytes(self.data) if bytes(self.data) else bytes(Bool(0))

	def __str__(self):
		return str(self.data)

	def isempty(self):
		if not self.data:
			return True
		return not bool(bytes(self.data))


class ExtensionsComment:	#ok

	def __init__(self, d):
		self.data = d

	def __bytes__(self):
	
		b = varint(len(self.data))
		for value in self.data:
			b += varint(value[0])

			if value[0] == 0:
				b += bytes(Beneficiaries(value[1]["beneficiaries"]))
			elif value[0] == 1:
				b += bytes(Uint64(value[1]["destination"]))
			elif value[0] == 2:
				b += bytes(Uint16(value[1]["percent"]))
	
		return b

	def __str__(self):
		return str(self.data)


class ArrayString:	#ok
	def __init__(self, d):
		self.data = d
		self.length = Varint32(len(self.data))

	def __bytes__(self):
		return bytes(self.length) + b"".join([bytes(String(a)) for a in self.data])
		#return bytes(self.length) + b"".join([varint(len(a)) + bytes(a, 'utf-8') for a in self.data])

	def __str__(self):
		r = []
		for a in self.data:
			if isinstance(a, ObjectId):
				r.append(str(a))
			elif isinstance(a, VoteId):
				r.append(str(a))
			elif isinstance(a, String):
				r.append(str(a))
			else:
				r.append(JsonObj(a))
		return json.dumps(r)

class APICache:
	def __init__(self):
		self.num_objects = 0
		self.stored_objects = []

class CacheDataMember:
	def __init__(self):
		self.expiration = 0
		self.ticker = ""
		self.data = {}
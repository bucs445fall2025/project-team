class CacheType:
	class CacheData:
		def __init__(self, value):
			self.lifespan = 0
			self.value = value
	def __init__(self):
		self.data = {}
	def get(key):
		if key in self.data:
			return self.data[key]
		return None
	def set(key, value):
		self.data[key] = value


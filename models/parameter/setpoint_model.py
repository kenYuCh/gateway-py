




class SetpointParams():
	def __init__(self):
		super().__init__()
		self.setpoint = 0
		self.switch = 0
		self.alaram = 0
		self.pair_1 = 0
		self.pair_2 = 0
		
	def get(self):
		pass
		
	def set(self, key, value):
		setattr(self, key, value)
	
	def load(self):
		pass
		
	def save(self):
		pass
		
	def update(self):
		print(f'Update: {self.port}')
		pass
		
	def printf(message:str):
		pass
		
	
a = SetpointParams()
a.set('pair_1', 456)
print(a.pair_1)

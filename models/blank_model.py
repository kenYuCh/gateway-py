



class BlankModel():
	def __init__(self):
		super().__init__()
		self.port = 0
		self.serial_number = "0000000000"
		self.value_count = 1
		self.name = ["blank"]
		self.value = [0]
		self.filter_enable = [False]
		self.measure_enable = False

	def get(self, key):
		return getattr(self, key)
		
	def set(self, key, value):
		setattr(self, key, value)
	
	def load(self):
		pass
		
	def save(self):
		pass
		
	def get_port(self):
		return self.port
	def set_port(self, port):
		return self.port

	def get_serial_number(self):
		return self.serial_number
	def set_serial_number(self, value):
		self.serial_number = value
		
	def get_measure_state(self):
		return self.measure_enable
	def set_measure_state(self):
		return self.measure_enable
		
	def get_filter_enable(self, index, value):
		return self.filter_enable[index, value]
	def set_filter_enable(self, index, value):
		self.filter_enable[index, value]
	
	def update(self):
		print(f'Update: {self.port}')
		pass
		
	def print_message(self):
		print(f'Port {self.port}: none')
	

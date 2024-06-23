
from .tools import convert_to_byte

class SwitchValveModel():
	def __init__(self):
		super().__init__()
		self.port = 0
		self.serial_number = "0000000000"
		self.value_count = 3
		self.on_timer = 0
		self_interval_time = 0
		self.count = 0
		self.mode = 0
		self.trigger = 0
		self.current_state = 0
		self.measure_enable = False
		self.memory_map = ['00' for i in range(64)]
		self.load()

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
		self.port = port

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
		
	def set_memory_map(self, memory_map):
		self.memory_map = memory_map
	def get_memory_map(self):
		return self.memory_map	
		
	def update(self):
		self.current_state = convert_to_byte(self.memory_map[4])
		self.mode = convert_to_byte(self.memory_map[6])
		self.trigger = convert_to_byte(self.memory_map[7])
		self.on_time = convert_to_byte(self.memory_map[8:10])
		self.interval_time = convert_to_byte(self.memory_map[10:12])

	def print_message(self):
		print(f'Port: {self.port} - {self.serial_number} \n'+
			f'current_state:{self.current_state}\n' +
			f'mode:{self.mode}\n'	  +
			f'trigger:{self.trigger}\n'  +
			f'on_time:{self.on_time}\n'  +
			f'interval_time:{self.interval_time}\n' 
		)


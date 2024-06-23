
from .tools import convert_to_byte
class SimuAirModel():
	def __init__(self):
		super().__init__()
		self.port = 0
		self.serial_number = ""
		self.value_count = 3
		self.name = ["temp", "rh", "co2"]
		self.value = [0, 0, 0]
		self.filter_enable = [False, False, False]
		self.measure_enable = False
		self.memory_map = ['00' for i in range(64)]
		self.load()
		print("SimuAirModel init")

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
		self.value[0] = convert_to_byte(self.memory_map[0:2])
		self.value[1] = convert_to_byte(self.memory_map[2:4])
		self.value[2] = convert_to_byte(self.memory_map[4:6])

	def print_message(self):
		print(f'Port: {self.port} - {self.serial_number} \n'+
			f'Temp:{self.value[0]}\n' +
			f'Rh:{self.value[1]}\n'	  +
			f'CO2:{self.value[2]}\n'  
		)




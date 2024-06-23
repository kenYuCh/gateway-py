from i2c_master import i2c_read_byte, i2c_write_byte, i2c_write_byte_array
import time
from thread_lock import lock
import configuration as config
import asyncio

DEVICE_ADDRESS = 0x68
DEVICE_READ = 0xFE
DEVICE_SERIAL_START_AT=0x39

bytes_length = 64

mesh_data_array = [0 for _ in range(config.MAX_PORT)]


def convert_to_hex_string(array:list): 
	hex_list = [f'{num:02X}' for num in array]
	return hex_list
def conbine_hex_string(array:list): 
	string = ''.join([item for item in array])
	return string
		
# Dump memory - every 16 byte wrap line.
def dump_memory(port, data_array:list):
	for i in range(0, len(data_array), 16):
		hex_line = ' '.join(f'{byte:02X}' for byte in data_array[i:i+16])
		print(hex_line)
		
#-------------------------------------------------------------------
# port 0~48
# Example: operate port-1 device, you can set select_device_port(1)
def select_device_port(port):
		i2c_write_byte(DEVICE_READ, port) # 0xFE, 0x02

# Example: set valve mode: port, 0x06, 0~255
def set_mesh_data_register_byte1(port, register_addr, data:int):
		try:
			with lock:
				byte_represe = data.to_bytes(length=1, byteorder='big')
				select_device_port(port)
				i2c_write_byte(register_addr, data)
		except Exception as e:
			print("set_mesh_data_register_byte1: ", e)
				
# Example: set valve on_time 300s: port, 0x08, 0~65535
def set_mesh_data_register_byte2(port, register_addr, data:int):
		try:
			with lock:
				byte_represe = data.to_bytes(length=2, byteorder='big')
				select_device_port(port)
				i2c_write_byte_array(register_addr, list(byte_represe))
		except Exception as e:
			print("set_mesh_data_register_byte2: ", e)

# Not specify: you can read any length.
def get_mesh_data_register(port, register_addr, length):
	try:
		select_device_port(port)
		mm = i2c_read_byte(register_addr, length)
		return mm
	except Exception as e:
		print("get_mesh_data_register: ", e)
# Example: get valve mode: port, 0x06, 0~255
def get_mesh_data_register_byte1(port, register_addr):
		try:
			select_device_port(port)
			mm = i2c_read_byte(register_addr, 1)
			interger_data = int.from_bytes(mm)
			return interger_data
		except Exception as e:
			print("get_mesh_data_register_byte1: ", e)
# Example: get valve on_time 300s: port, 0x08
def get_mesh_data_register_byte2(port, register_addr):
		try:
			select_device_port(port)
			mm = i2c_read_byte(register_addr, 2)
			interger_data = int.from_bytes(mm)
			return interger_data
		except Exception as e:
			print("get_mesh_data_register_byte2: ", e)
#-------------------------------------------------------------------
def get_mesh_data_from_array(port):
		try:
			if port < len(mesh_data_array):
				return mesh_data_array[port]
		except Exception as e:
			print("get_mesh_data_from_array: ", e)
# Example: get device serial, get -> 50018500B1
def get_device_serial(port):
	try:
		# because mesh_data_list default value is 0, so need to check. 
		if mesh_data_array[port] != 0:
			mesh_data = get_mesh_data_from_array(port)
			merged_hex_string5 = conbine_hex_string(mesh_data[57:62])
			return merged_hex_string5
		#integer_array = get_mesh_data_register(port, DEVICE_SERIAL_START_AT, 5)
		#hex_list = convert_to_hex_string(integer_array)
		#merged_hex_string = ''.join(hex_list)
		#return merged_hex_string
	except Exception as e:
		print("get_device_serial: ", e)
		
# Example: get device type, get -> 50
# use get_mesh_data_from_memory_map() get memory data than get device type.
def get_device_type(hex_string_memory_map):
		try:
			return hex_string_memory_map[57:58][0]
		except Exception as e:
			print("get_device_type: ", e)

	
# Example: get mesh data at port,  
def get_mesh_data_from_memory_map(port):
		try:
			read_data = []
			select_device_port(port)
			hex_data = []
		
			for offset2 in range(0, bytes_length, 32):
				chunk_size = min(32, bytes_length - offset2)
				data_chunk = i2c_read_byte(0x00 + offset2, 32)
				# dump
				if config.enable_dump == True:
					dump_memory(port, data_chunk)
				hex_data.extend(data_chunk)
				
			hex_string_list = convert_to_hex_string(hex_data)
			return hex_string_list
		except Exception as e:
			print("get_mesh_data_from_memory_map: ", e)
	 
# Example: update memory map at all port.
def update_mesh_data():
	try:
		for i in range(config.MAX_PORT):
			data = get_mesh_data_from_memory_map(i)
			mesh_data_array[i] = data
	except Exception as e:
		print("update_mesh_data: ", e)


# set parameter 

# set_mesh_data_register(port, register, data)
# set_mesh_data_register_byte16(port, register, data)
# get_mesh_data_from_memory_map(port)
# get_device_serial(port)
# get_mesh_data_register_byte16(port, register_addr_int)

set_mesh_data_register_byte1(2, 0x06, 2)			# mode	  : 0,1,2
set_mesh_data_register_byte1(2, 0x07, 1)			# trigger : 1
set_mesh_data_register_byte2(2, 8, 300)	# on_time : test 10~300
set_mesh_data_register_byte2(2, 10, 300) # interval : test 10~300
#mm = get_mesh_data_from_memory_map(2) # (port, start_read_byte, read_length)

device_serial = get_device_serial(2)
mode = get_mesh_data_register_byte1(2, 6)
on_time = get_mesh_data_register_byte2(2, 8)
interval_time = get_mesh_data_register_byte2(2, 10)
#device_type = get_device_type(mm)

#print("Device_serial: ", device_serial)
#print("Device_tyoe: ", device_type)
#print("Device: mode -> ", mode)
#print("Device: on_time -> ", on_time)
#print("Device: device_type -> ", interval_time)

#print("Device: value_memory_map -> ", mesh_data_array[2])


# async run mesh data process main.

#asyncio.run(mesh_data_process_main())

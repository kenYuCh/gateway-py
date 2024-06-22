from i2c_master import i2c_read_byte, i2c_write_byte, i2c_write_byte_array
import time
import threading
lock = threading.Lock()

DEVICE_ADDRESS = 0x68
DEVICE_READ = 0xFE
DEVICE_SERIAL_START_AT=0x39
MAX_PORTS = 12
bytes_length = 64

mesh_data_array = []


def convert_to_hex_string(array:list): 
	hex_list = [f'{num:02X}' for num in array]
	return hex_list
#-------------------------------------------------------------------
# port 0~48
# Example: operate port-1 device, you can set select_device_port(1)
def select_device_port(port):
	i2c_write_byte(DEVICE_READ, port) # 0xFE, 0x02

# Example: set vavle mode: port, 0x06, 1
def set_mesh_data_register(port, register_addr, data:int):
	byte_represe = data.to_bytes(length=1, byteorder='big')
	select_device_port(port)
	i2c_write_byte(register_addr, data)
	
# Example: set vavle on_time 300s: port, 0x08, 300
def set_mesh_data_register_byte16(port, register_addr, data:int):
	byte_represe = data.to_bytes(length=2, byteorder='big')
	select_device_port(port)
	i2c_write_byte_array(register_addr, list(byte_represe))
	
def get_mesh_data_register(port, register_addr, length):
	select_device_port(port)
	mm = i2c_read_byte(register_addr, length)
	return mm
	
def get_mesh_data_register_byte8(port, register_addr):
	select_device_port(port)
	mm = i2c_read_byte(register_addr, 1)
	interger_data = int.from_bytes(mm)
	return interger_data
	
# Example: get vavle on_time 300s: port, 0x08, 300
def get_mesh_data_register_byte16(port, register_addr):
	select_device_port(port)
	mm = i2c_read_byte(register_addr, 2)
	interger_data = int.from_bytes(mm)
	return interger_data
	
#-------------------------------------------------------------------
def get_mesh_data_from_array(port):
	if port < len(mesh_data_array):
		return mesh_data_array[port]

# Example: port, get string -> 50018500B1
def get_device_serial(port):
	integer_array = get_mesh_data_register(port, DEVICE_SERIAL_START_AT, 5)
	hex_list = convert_to_hex_string(integer_array)
	merged_hex_string = ''.join(hex_list)
	return merged_hex_string
	
# Example: port, get string -> 50
def get_device_type(hex_string_memory_map):
	return hex_string_memory_map[57:58][0]
	
def get_mesh_data_from_memory_map(port):
    read_data = []
    select_device_port(port)
    for offset in range(0, bytes_length, 32):
        chunk_size = min(32, bytes_length - offset)
        data_chunk = i2c_read_byte(0x00 + offset, chunk_size) # 0x00 at read start
        read_data.extend(data_chunk)
    #read_data = [num.to_bytes(1, byteorder='big') for num in read_data]
    hex_string_list = convert_to_hex_string(read_data)
    return hex_string_list
    
def update_mesh_data():
    try:
        for i in range(MAX_PORTS):
            data = get_mesh_data_from_memory_map(i)
            mesh_data_array.insert(i, data)
        print(f'{mesh_data_array} \r\n') 
    except IOError as e:
        print(f'I/O error: {e}')


def update_mesh_data_task():
	while True:
		with lock:
			update_mesh_data()
		time.sleep(2)
    

# set parameter 

# set_mesh_data_register(port, register, data)
# set_mesh_data_register_byte16(port, register, data)
# get_mesh_data_from_memory_map(port)
# get_device_serial(port)
# get_mesh_data_register_byte16(port, register_addr)

set_mesh_data_register(2, 0x06, 2)			# mode	  : 0,1,2
set_mesh_data_register(2, 0x07, 1)			# trigger : 1
set_mesh_data_register_byte16(2, 8, 30)	# on_time : test 10~300
set_mesh_data_register_byte16(2, 10, 10) # interval : test 10~300
mm = get_mesh_data_from_memory_map(2) # (port, start_read_byte, read_length)
print(mm)

device_serial = get_device_serial(2)
mode = get_mesh_data_register_byte8(2, 6)
on_time = get_mesh_data_register_byte16(2, 8)
interval_time = get_mesh_data_register_byte16(2, 10)
device_type = get_device_type(mm)

print("Device_serial: ", device_serial)
print("Device_tyoe: ", device_type)
print("Device: mode -> ", mode)
print("Device: on_time -> ", on_time)
print("Device: device_type -> ", interval_time)






















#update_mesh_data()
#t = get_mesh_data_from_array(3)
#print(t)


#update_mesh_data_task()

#memory_select_port(3)
#data = get_memory_map(DEVICE_READ, 3)
#print(data)


#memory_register_set(2, 0x06) # port, register

# write_byte(0x68, 0xFE, 0x02)
# write_byte(0x68, 0x06, 0x00)
# write_byte_array(0x68, 0x06, [0x01, 0x00, 0x00])












































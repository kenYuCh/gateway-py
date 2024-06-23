from models.blank_model import BlankModel
from models.switch_valve_model import SwitchValveModel
from models.simuair_model import SimuAirModel
from mesh_data_process import mesh_data_array, get_device_type, get_device_serial
import configuration as config
import asyncio

model_object_list = [0 for _ in range(config.MAX_PORT)]

select_device_type = {
	"AC": SimuAirModel(),
	"50": SwitchValveModel(),
	'blank': BlankModel()
}

def is_check_model(device_type):
	if device_type != "00":
		return True
	else:
		return False

def get_model(port):
	model = model_object_list[port] 
	return model

def set_model(port):
	mm = mesh_data_array[port]
	device_type = get_device_type(mm)
	if is_check_model(device_type):
		model_object_list[port] = select_device_type[device_type]
		model = model_object_list[port]
		model.set_port(port)
		model.set_serial_number(get_device_serial(port))
		model.set_memory_map(mm)
		model.update()
		model.print_message()
	else:
		model_object_list[port] = select_device_type['blank']
		model_object_list[port].port = port
	
	
def update_model():
	for port in range(len(mesh_data_array)):
		print(f"--------------- '{port}' -----------\r\n")
		set_model(port)
	




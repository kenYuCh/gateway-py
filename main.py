from mesh_data_process import update_mesh_data
from model import update_model
import asyncio
import time
import subprocess
import configuration as config
state = {
	"is_wifi_connected": False,
	"is_mqtt_connected": True,
	"is_complete": False
}

def set_state(key, value):
	state[key] = value
	
def get_state(key):
	return state[key]
	
def is_setting_complete():
	if get_state('is_wifi_connected') and get_state('is_mqtt_connected'):
		return True
	else:
		return False
		
#----------------------------------------------------------
# Example: every X sec update one times all MemoryMap.
async def update_mesh_data_task(every_sec):
	try:
		while True:
			update_mesh_data()
			await asyncio.sleep(every_sec)
	except Exception as e:
		print("update_mesh_data_task: ", e)
		
		
# Example: every X sec update one times all ModelObject.
async def update_model_task(every_sec):
	try:
		while True:
			update_model()
			await asyncio.sleep(every_sec)
	except Exception as e:
		print("update_mesh_data_task: ", e)

#----------------------------------------------------------
def is_wifi_connected():
	try:
		result = subprocess.run(['iwconfig'], capture_output=True, text=True)
		output = result.stdout
		if config.wifi_setting['ssid'] in output:
			# print("WIFI is connected.")
			return True
		else:
			print("WIFI is not connected.")
			return False
	except Exception as e:
		print("WIFI Error occurred: ", e)
		return False
		
async def is_wifi_connected_task():
	while True:
		set_state('is_wifi_connected', is_wifi_connected())
		await asyncio.sleep(1)
		

#----------------------------------------------------------
async def run_task():
	task0 = asyncio.create_task(is_wifi_connected_task())
	first = 0
	while True:
		if is_setting_complete() == True and first == 0:
			first = 1
			task3 = asyncio.create_task(update_mesh_data_task(3))
			task4 = asyncio.create_task(update_model_task(5))

		await asyncio.sleep(1)
		
if __name__ == "__main__":
	print("System setting...")
	asyncio.run(run_task())

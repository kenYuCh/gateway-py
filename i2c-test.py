#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  i2c-test.py
#  
#  Copyright 2024  <ken@ken>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
#
import sys
import smbus2
import time

DEVICE_ADDRESS = 0x68
MAX_PORTS = 12

num_bytes = 64
register_address = 0x00
bus = smbus2.SMBus(1)

mesh_memory_array_data = [] # [port][mesh_data_byte]

def read_byte(device_addr, register_addr):
    return bus.read_byte_data(device_addr, register_addr)

def read_byte_array(device_addr, register_addr, length):
    return bus.read_i2c_block_data(device_addr, register_addr, length)

def write_byte(device_addr, register_addr, data):
    bus.write_byte_data(device_addr, register_addr, data)
    
def write_byte_array(device_addr, register_addr, data:list):
    bus.write_i2c_block_data(device_addr, register_addr, data)

# write_byte(0x68, 0xFE, 0x03) # air
# write_byte(0x68, 0xFE, 0x02) # valve

def get_memory_map(device_addr, register_addr, port):
    read_data  = []
    write_byte(device_addr, register_addr, port)
    for offset in range(0, num_bytes, 32):
        chunk_size = min(32, num_bytes - offset)
        data_chunk = read_byte_array(DEVICE_ADDRESS, register_address + offset, chunk_size)
        read_data.extend(data_chunk)
    return read_data
    
def update_memory_map():
    try:
        for i in range(MAX_PORTS):
            data = get_memory_map(0x68, 0xFE, i)
            #print(f'{data}') 
            mesh_memory_array_data.insert(i, data)
        print(f'{mesh_memory_array_data}') 
    except IOError as e:
        print(f'I/O error: {e}')
    
def main(args):
    try:
        while True:
            update_memory_map()
            time.sleep(2)
    except KeyboardInterrupt:
        print("error")
        

if __name__ == '__main__':
    sys.exit(main(sys.argv))

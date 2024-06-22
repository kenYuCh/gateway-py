#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  i2c_master.py
#  
#  Copyright 2024  <ken@gmail.com> !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
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
DEVICE_READ = 0xFE

bus = smbus2.SMBus(1)

# DEVICE_ADDRESS, START_AT_READ, READ_LENGTG 

def i2c_read_byte(register_addr, length):
    return bus.read_i2c_block_data(DEVICE_ADDRESS, register_addr, length)

def i2c_write_byte(register_addr, data):
    bus.write_byte_data(DEVICE_ADDRESS, register_addr, data)
    
def i2c_write_byte_array(register_addr, data:list):
    bus.write_i2c_block_data(DEVICE_ADDRESS, register_addr, data)


    
# write_byte(0x68, 0xFE, 0x03) # air
# write_byte(0x68, 0xFE, 0x02) # valve



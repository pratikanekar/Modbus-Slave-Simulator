#!/usr/bin/env python
# scripts/examples/simple_data_store.py
from loguru import logger
import socket
from socketserver import TCPServer
from collections import defaultdict

import redis
from umodbus import conf
from umodbus.server.tcp import RequestHandler, get_server
from umodbus.utils import log_to_stream
import time
from _thread import *
from typing import Union
from fastapi import FastAPI
from uvicorn import run
random_open = {"01": "c", "02": "discrete_input", "03": "h", "04": "i"}

# A very simple data store which maps addresses against their values.
data_store = defaultdict(int)
data_store[0]=111
data_store[1]=222
data_store[2]=333
data_store[3]=444
data_store[40001]=444

x=0
y=0
xx=0
yy=0

def set_xx(value):
    global xx
    xx=value

def get_xx():
    global xx
    return xx

def set_yy(value):
    global yy
    yy=value

def get_yy():
    global yy
    return yy


def redis_database(function_code, start_address):
    try:
        redis_ip = "192.168.1.205"
        redis_port = 6379
        start_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        start_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        redis_db_conn = redis.Redis(host=redis_ip, port=redis_port)
        if redis_db_conn.ping():
            logger.debug(f"Done connection with Redis Database IP:{redis_ip} Port:{redis_port}")
            reg_values = redis_db_conn.get(f"{random_open[function_code]}_{start_address}")
            return reg_values
    except Exception as e:
        pass



# Add stream handler to logger 'uModbus'.
#log_to_stream(level=logging.DEBUG)
    
# Enable values to be signed (default is False).
conf.SIGNED_VALUES = True

TCPServer.allow_reuse_address = True
app = get_server(TCPServer, ('0.0.0.0',     502), RequestHandler)


@app.route(slave_ids=[1], function_codes=[1,2,3], addresses=list(range(0, 100)))
def read_data_store(slave_id, function_code, address):
    """" Return value of address. """
    global data_store
    global y 
    data_store[0]=111
    data_store[1]=222
    data_store[2]=get_yy()
    data_store[20]=138
    data_store[21]=74
    y=y+1
    set_yy(get_yy()+1)
    print(data_store,"---",data_store[address])
    print(slave_id,function_code,address)
    print("modbus xx yy",get_xx(),get_yy())
    return data_store[address]

@app.route(slave_ids=[1], function_codes=[5, 15], addresses=list(range(0, 10)))
def write_data_store(slave_id, function_code, address, value):
    """" Set value for address. """
    data_store[address] = value


def starrt_modbus_server():
    print("Start Modbus")
    print("Testing Debug")
    try:
        app.serve_forever()
    finally:
        app.shutdown()
        app.server_close()

#------------------------ FAST API ----------------
fastapi = FastAPI()
@fastapi.get("/")
def read_root():
    global x 
    global y
    x=x+1
    set_xx(get_xx()+1)
    return {"Hello": "World --> "+str(get_xx())+"  "+str(get_yy())+str(data_store)}

@fastapi.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@fastapi.on_event("startup")
async def init_processes():
    #start_new_thread(starrt_modbus_server, ())
    pass




if __name__ == '__main__':
    start_new_thread(starrt_modbus_server, ())
    run("fastapi-mod:fastapi", host="0.0.0.0", port=5017, reload=True)
    

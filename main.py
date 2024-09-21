from loguru import logger
import socket
from socketserver import TCPServer
from collections import defaultdict
import redis
from umodbus import conf
from umodbus.server.tcp import RequestHandler, get_server
import argparse
from create_csv_add_data_redis.create_redis_db_and_push_data import add_data_into_redis_db

"""
    Here we can Set up argument parsing for command-line inputs
"""

parser = argparse.ArgumentParser()
parser.add_argument("-ModbusPort", "--mport", help="Enter the Port that you want to Expose for Slave", type=int,
                    default=1502)
parser.add_argument("-RedisDB", "--redisdb", help="Enter the Redis DB", type=int, default=0)
parser.add_argument("-CreateRedisDB", "--newredisdb",
                    help="Set this to true if you want to create a new db with new data", type=bool, default=False)
args = parser.parse_args()

"""
    Here we crate Modbus Function Type Mapping 
"""
car_map = {"coils": "c", "holding": "h", "input": "i"}
file_names = ["coils", "holding", "input"]
random_open = {1: "c", 2: "discrete_input", 3: "h", 4: "i"}

"""
    Following Redis connection setup
"""
redis_ip = "10.129.2.23"  # change ip according to redis is hosted ip
redis_port = 6379
redis_db = args.redisdb
modbus_port = args.mport

"""
    Following line is used to connect the Redis Database
"""
redis_db_conn = redis.Redis(host=redis_ip, port=redis_port, db=redis_db)

"""
Initialize data store for Modbus addresses
"""
data_store = defaultdict(int, {0: 111, 1: 222, 2: 333, 3: 444, 4: 444, 21: 78})


def check_create_redis_db():
    """
        In this function we create newly redis database and add data into DB using CSV file
    """
    add_data_into_redis_db()


def read_val_redis_database(function_code, start_address):
    """
        In this function we get value from redis database using function code and addresses
    """
    try:
        start_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        start_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        if redis_db_conn.ping():
            logger.debug(f"Done connection with Redis Database IP - {redis_ip} Port - {redis_port}")
            reg_values = redis_db_conn.get(f"{random_open[function_code]}_{start_address}")
            return reg_values
    except Exception as e:
        logger.error(f"Error Occurred in the redis connection read_val_redis_database - {e}")


def write_val_redis_database(function_code, start_address, value):
    """
        In this function we write value redis database using function code and addresses
    """
    try:
        start_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        start_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        if redis_db_conn.ping():
            logger.debug(f"Done connection with Redis Database IP - {redis_ip} Port - {redis_port}")
            redis_db_conn.set(f"{random_open[function_code]}_{start_address}", value=value)
        logger.info(f"Modbus Register Write successful")
    except Exception as e:
        logger.error(f"Error Occurred in the redis connection write_val_redis_database - {e}")


"""
    Here Configure Modbus server
"""
conf.SIGNED_VALUES = True
TCPServer.allow_reuse_address = True
app = get_server(TCPServer, ('0.0.0.0', modbus_port), RequestHandler)


@app.route(slave_ids=[1], function_codes=[1, 2, 3, 4], addresses=list(range(0, 1000)))
def read_data(slave_id, function_code, address):
    """
        In this Function we read data from redis database and return to callable function
    """
    global data_store
    logger.debug(f"Request Data from modbus slave_id - {slave_id} func_code - {function_code} address - {address}")
    redis_value = read_val_redis_database(function_code, address)
    decoded_value = int(redis_value.decode()) if redis_value else 0

    # if decoded_value >= 32768:
    #     logger.debug(f"Negative value received so we convert it into positive value - {decoded_value}")
    #     decoded_value = (65536 - decoded_value) * -1

    logger.debug(f"Modbus address {address} value: {decoded_value}")
    data_store[address] = decoded_value
    return decoded_value


@app.route(slave_ids=[1], function_codes=[1, 3, 4, 6, 16], addresses=list(range(0, 1000)))
def write_data(slave_id, function_code, address, value):
    """
        In this Function we Write data in redis database
    """
    logger.debug(
        f"Write Modbus Data slave_id - {slave_id} func_code - {function_code} address - {address} and Value - {value}")
    write_val_redis_database(function_code, address, value)


def start_modbus_server():
    """
        In this function we start the Modbus simulator
    """
    logger.info(f"Started Modbus TCP Simulator on PORT number - {modbus_port}")
    try:
        app.serve_forever()
    finally:
        app.shutdown()
        app.server_close()


if __name__ == '__main__':
    logger.info(f"Connected to redis_ip - {redis_ip} , redis_port - {redis_port} , redis_db - {redis_db}")
    logger.debug(f"For testing use following $pymodbus.console tcp --host localhost --port 1502")
    if args.newredisdb:
        check_create_redis_db()

    # Start the Modbus simulator
    start_modbus_server()

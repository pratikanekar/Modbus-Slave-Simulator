import csv
import redis
import os
from loguru import logger

redis_ip = "192.168.1.205"
redis_port = 6379

redis_db_conn = redis.Redis(host=redis_ip, port=redis_port, db=1)

car_map = {"coils": "c", "holding": "h", "input": "i"}

file_names = ["coils", "holding", "input"]

for file_name in file_names:
    file_open = open(f"{os.getcwd()}/modbus/{file_name}.csv", "r")
    file_reader = csv.reader(file_open)
    logger.info(f"Processing Data for File: {file_name}")
    for row in file_reader:
        # set the Row[0] as h_val  and value as row[1]
        if redis_db_conn.ping():
            redis_db_conn.set(f"{car_map[file_name]}_{row[0]}", row[1])
    logger.info(f"Done With File: {file_name}")

import csv
import redis
import os
from loguru import logger

redis_ip = "192.168.1.219"  # change ip according to redis is hosted ip
redis_port = 6379
redis_db_conn = redis.Redis(host=redis_ip, port=redis_port, db=0)
car_map = {"coils": "c", "holding": "h", "input": "i"}
file_names = ["coils", "holding", "input"]


def add_data_into_redis_db():
    """
        This function is used to create redis database and using the holding, input, coil register csv,
        add data into redis database
    """
    for file_name in file_names:
        file_open = open(f"{os.getcwd()}/{file_name}.csv", "r")
        file_reader = csv.reader(file_open)
        logger.info(f"Processing Data for File: {file_name}")
        for row in file_reader:
            # set the Row[0] as h_val  and value as row[1]
            if redis_db_conn.ping():
                redis_db_conn.set(f"{car_map[file_name]}_{row[0]}", 0)
        logger.info(f"Done With File: {file_name}")


if __name__ == '__main__':
    add_data_into_redis_db()

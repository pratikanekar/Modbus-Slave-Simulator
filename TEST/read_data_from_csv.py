import random
import csv
from os import getcwd
from loguru import logger
from time import sleep


def make_register_dict(register_type: str, start_reg_addr=1, end_reg_addr=65537, start_val=0, end_val=65535):
    register_key_val = {}
    file_ = None
    path = f"{getcwd()}/modbus/{register_type}.csv"
    try:
        for i in range(start_reg_addr, end_reg_addr):
            random_val = random.randint(start_val, end_val)
            register_key_val.update({i: random_val})
        file_ = open(path, "w+")
        writer = csv.writer(file_)
        for j in register_key_val:
            writer.writerow([j, register_key_val.get(j)])
        logger.debug(f"Done file creation of {path}")
    except Exception as e:
        logger.error(f"Error on {path}: {e}")
    finally:
        if file_ is not None:
            file_.close()
        sleep(2)


if __name__ == '__main__':
    make_register_dict(register_type="holding")
    make_register_dict(register_type="input")
    make_register_dict(register_type="coils", start_val=0, end_val=1)

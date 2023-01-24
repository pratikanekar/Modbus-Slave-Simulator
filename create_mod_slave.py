import serial
from loguru import logger
from math import ceil
import csv
from os import getcwd

# following object is used to for serial communication
# receiver = serial.Serial(
#      port='/dev/ttyUSB0',
#      baudrate=57600,
#      parity=serial.PARITY_NONE,
#      stopbits=serial.STOPBITS_ONE,
#      bytesize=serial.EIGHTBITS,
#      timeout=1
#      )
all_register_dict = {"holding": {}, "input": {}, "coils": {}}

for file_name in all_register_dict:
    file_open = open(f"{getcwd()}/modbus/{file_name}.csv", "r")
    file_reader = csv.reader(file_open)
    for row in file_reader:
        all_register_dict.get(file_name).update({row[0]: row[1]})
    file_open.close()
random_open = {"01": "coils", "02": "discrete_input", "03": "holding", "04": "input"}


# following function is used to finding values of starting addresses
def find_start_add_value(st_add, function_code, mod_count):
    try:
        start_address = int(f"{st_add}", 16)
        # start_address = int(f"0x{st_add}", 0)
        addresses = []
        for row in all_register_dict:
            if row == random_open.get(function_code):
                final_count = int(f"0x{mod_count}", 0)
                for i in range(final_count):
                    reg_values = int(all_register_dict.get(row).get(str(start_address)))
                    start_address = start_address + 1
                    addresses.append(hex(reg_values).replace("0x", ""))
        final_address = ("".join(addresses))
        return final_address
    except Exception as e:
        logger.error(f"error occurred in find_start_add_value as : {e}")


# following function is used to find bytecount of modbus
def find_count_register(mod_count, funtion_code):
    try:
        if funtion_code == "01" or funtion_code == "02":
            temp = int(f"0x{mod_count}", 0)
            require_byte = ceil(temp/8) + 1
            count_val = hex(require_byte).replace("x", "")
            return count_val
        elif funtion_code == "03" or funtion_code == "04":
            temp = int(f"0x{mod_count}", 0)
            require_byte = ceil((temp * 16) / 8)
            count_val = hex(require_byte).replace("x", "")
            return count_val
    except Exception as e:
        logger.error(f"error occurred in find_count_register as : {e}")


# following function is used to decoding receive data for calculation
def decode_data_fun(received_data):
    try:
        received_data = received_data.split("\\x")
        slave_id = received_data[1]                        # here we find slave_id from received data
        function_code = received_data[2]                   # here we find function_code from received data
        st_add = received_data[3] + received_data[4]      # here we find starting_address from received data
        mod_count = received_data[5] + received_data[6]
        count = find_count_register(mod_count, function_code)   # here we find byte_count from received data
        # checksum = x.split("\\x")[7] + x.split("\\x")[8].replace("'", "")
        start_add = find_start_add_value(st_add, function_code, mod_count)  # here we call function for give addresses
        data = f"{slave_id}{function_code}{count}{start_add}"
        checksum = crc16(data).replace(" ", "0")                # here we find crc16(checksum) for sending data
        return f"{data}{checksum}"
    except Exception as e:
        logger.error(f"error occurred in decode_data_function as : {e}")


# following function is used to calculate the checksum(crc16)
# reference  :--  https://forums.swift.org/t/2-questions-about-modbus-function-conversion-and-a-socket-library/13048
def crc16(data, bits=8):
    try:
        crc = 0xFFFF
        for op, code in zip(data[0::2], data[1::2]):
            crc = crc ^ int(op+code, 16)
            for bit in range(0, bits):
                if (crc & 0x0001) == 0x0001:
                    crc = ((crc >> 1) ^ 0xA001)
                else:
                    crc = crc >> 1
        msb = crc >> 8
        lsb = crc & 0x00FF
        return '{:2x}{:2x}'.format(lsb, msb)
    except Exception as e:
        logger.error(f"error occurred in crc16 as : {e}")


if __name__ == '__main__':
    try:
        # Make a function to store a in dict
        # while 1:
        # received_data = receiver.readline()
        received_data = str(b'\x01\x04\x00\x0e\x00\x04\xcc\x19')
        logger.info(f"Received Data From Modbus : {received_data}")
        send_data = decode_data_fun(received_data)
        logger.info(f"Send Data To Modbus : {send_data}")
    except Exception as e:
        logger.error(f"error occurred in main as : {e}")
    except KeyboardInterrupt:
        logger.error(f"Found KeyBoard Interrupt,so EXIT Code")
        # break

import serial
from loguru import logger
from math import ceil
import csv
from os import getcwd
# receiver = serial.Serial(
#      port='/dev/ttyUSB0',
#      baudrate=57600,
#      parity=serial.PARITY_NONE,
#      stopbits=serial.STOPBITS_ONE,
#      bytesize=serial.EIGHTBITS,
#      timeout=1
#      )

received_data = b'\x01\x04\x00\x0e\x00\x04\xcc\x19'
# starting_address = {1: 20859, 2: 40117, 14: 40950, 4: 5774, 124: 28399, 5894: 23}
# open_csv = {"01": "read_coil_status", "02": "read_input_status", "03": "read_holding_register", "04": "read_input_register"}
random_open = {"01": "coil", "02": "input_status", "03": "holding", "04": "input"}


# following function is used to finding values of starting addresses
def find_start_add_value(st_add, function_code, mod_count):
    file_path = f"{getcwd()}/modbus/{random_open.get(function_code)}.csv"
    file = open(f"{file_path}", "r")
    reader = csv.reader(file)
    start_address = int(f"0x{st_add}", 0)
    count = 0
    addresses = []
    for row in reader:
        # for i in range(count):
        final_count = int(f"0x{mod_count}", 0)
        if int(row[0]) == start_address and count < final_count:
            start_address = start_address + 1
            reg_values = int(row[1])
            addresses.append(hex(reg_values).replace("0x", ""))
            count = count + 1
        if count == final_count:
            break
    final_address = ("".join(addresses))
    return final_address


# following function is used to find bytecount of modbus
def find_count_register(mod_count, funtion_code):
    if (funtion_code == "01"):
        temp = int(f"0x{mod_count}", 0)
        require_byte = ceil(temp/8)+1
        count_val = hex(require_byte).replace("x", "")
        return count_val
    elif (funtion_code == "02"):
        temp = int(f"0x{mod_count}", 0)
        require_byte = ceil(temp / 8) + 1
        count_val = hex(require_byte).replace("x", "")
        return count_val
    elif (funtion_code == "03"):
        temp = int(f"0x{mod_count}", 0)
        require_byte = ceil((temp * 16) / 8) + 1
        count_val = hex(require_byte).replace("x", "")
        return count_val
    elif (funtion_code == "04"):
        temp = int(f"0x{mod_count}", 0)
        require_byte = ceil((temp * 16) / 8) + 1
        count_val = hex(require_byte).replace("x", "")
        return count_val



# following function is used to decoding receive data for calculation
def decode_data_fun(x):
    slave_id = x.split("\\x")[1]
    function_code = x.split("\\x")[2]
    st_add = x.split("\\x")[3] + x.split("\\x")[4]
    mod_count = x.split("\\x")[5] + x.split("\\x")[6]
    count = find_count_register(mod_count, function_code)
    # checksum = x.split("\\x")[7] + x.split("\\x")[8].replace("'", "")
    start_add = find_start_add_value(st_add, function_code, mod_count)
    data = f"{slave_id}{function_code}{count}{start_add}"
    checksum = crc16(data).replace(" ", "0")
    return f"{data}{checksum}"



# following fucntion is used to calculate the checksum(crc16)
# reference  :--  https://forums.swift.org/t/2-questions-about-modbus-function-conversion-and-a-socket-library/13048
def crc16(data, bits=8):
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


try:
    # while 1:
    # x = receiver.readline()
    x = str(received_data)
    logger.info(f"Received Data From Modbus : {received_data}")
    send_data = bytes.fromhex(decode_data_fun(x))
    logger.info(f"Send Data To Modbus : {send_data}")
except Exception as e:
    print(e)
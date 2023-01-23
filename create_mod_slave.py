import serial
from loguru import logger
# receiver = serial.Serial(
#      port='/dev/ttyUSB0',
#      baudrate=57600,
#      parity=serial.PARITY_NONE,
#      stopbits=serial.STOPBITS_ONE,
#      bytesize=serial.EIGHTBITS,
#      timeout=1
#      )

received_data = b'\x01\x04\x00\x0e\xff\x00\xcc\x19'
starting_address = {1: 20859, 2: 40117, 14: 40950, 4: 5774, 124: 28399, 5894: 23}
open_csv = {"01": "read_coil_status", "02": "read_input_status", "03": "read_holding_register", "04": "read_input_register"}


# following function is used to finding values of starting addresses
def find_start_add_value(st_add):
    temp = int(f"0x{st_add}", 0)
    value = hex(starting_address.get(temp)).replace("0x", "")
    return value


# following function is used to decoding receive data for calculation
def decode_data_fun(x):
    slave_id = x.split("\\x")[1]
    funtion_code = x.split("\\x")[2]
    st_add = x.split("\\x")[3] + x.split("\\x")[4]
    start_add = find_start_add_value(st_add)
    count = x.split("\\x")[5] + x.split("\\x")[6]
    # checksum = x.split("\\x")[7] + x.split("\\x")[8].replace("'", "")
    data = f"{slave_id}{funtion_code}{start_add}{count}"
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
    return '{:2X}{:2X}'.format(lsb, msb)


try:
    # while 1:
    # x = receiver.readline()
    x = str(received_data)
    logger.info(f"Received Data From Modbus : {received_data}")
    send_data = bytes.fromhex(decode_data_fun(x))
    logger.info(f"Send Data To Modbus : {send_data}")
except Exception as e:
    print(e)
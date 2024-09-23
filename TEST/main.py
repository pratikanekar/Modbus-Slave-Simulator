from create_mod_slave import read_csv_file as data_from_csv_file
from create_mod_slave import decode_data_fun
from loguru import logger
import serial

# following object is used to for serial communication
serial_reader = serial.Serial(
     port='/dev/ttyUSB0',
     baudrate=9600,
     parity=serial.PARITY_NONE,
     stopbits=serial.STOPBITS_ONE,
     bytesize=serial.EIGHTBITS
     )

logger.info(f"Program is started ...")
logger.info(f"Press 1 for Give Data from CSV file")
logger.info(f"Press 2 for Give Data from Redis Database")
user_choice = int(input(f"Please Enter Your Choice"))
# user_choice = 1
if user_choice == 1:
    data_from_csv_file()
elif user_choice == 2:
    pass
else:
    logger.debug(f"Please Enter valid choice ...")


if __name__ == '__main__':
    while 1:
        try:
            received_data = serial_reader.read(16)
            # received_data = b'\x01\x03\x00\x0a\x00\x08\x64\x0b'
            if len(received_data) > 0:
                try:
                    received_data = received_data.hex()
                except:
                    logger.debug(f"Error on Data: {received_data}")
                    continue

                logger.info(f"Received Data From Modbus : {received_data.upper()}")
                send_data = bytes.fromhex(decode_data_fun(received_data))
                serial_reader.write(send_data)
                logger.info(f"Send Data To Modbus : {send_data.hex().upper()}")
            else:
                logger.debug(f"No Data Found")
        except Exception as e:
            logger.error(f"error occurred in main as : {e}")
        except KeyboardInterrupt:
            logger.error(f"Found KeyBoard Interrupt,so EXIT Code")

        finally:
            serial_reader.flush()
            pass

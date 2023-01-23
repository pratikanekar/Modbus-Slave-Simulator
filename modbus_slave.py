from pymodbus.client.serial import ModbusSerialClient
from time import sleep
mod_baud_rate = [110, 300, 600, 1200, 2400, 4800, 9600, 14400, 19200, 38400, 57600, 115200, 128000, 256000]
mod_port = ["/dev/ttyUSB0", "/dev/ttyUSB1"]

try:
    for i in range(0, len(mod_port)):
        for j in range(0, len(mod_baud_rate)):
            try:
                mod_client = ModbusSerialClient(
                    method='rtu',
                    port=mod_port[i],
                    baudrate=mod_baud_rate[j],
                    timeout=3,
                    parity='N',
                    stopbits=1,
                    bytesize=8
                )
                if mod_client.connect():  # Trying for connect to Modbus
                    read_register = mod_client.read_holding_registers(address=0, count=2, unit=1)
                    mod_read_list = read_register.registers  # it is used to store input register values
                    print(f"Connected Registers {mod_read_list}")
                else:
                    print('Cannot connect to the Modbus')
            except Exception as e:
                sleep(0.1)
                pass
except Exception as e:
    pass

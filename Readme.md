# How to Use Modbus Slave Simulator:

1) First clone the repository name Modbus slave simulator 
```
Cmd - git clone https://github.com/pratikanekar/Modbus-Slave-Simulator.git
```
2) If docker, docker compose, redis, redis-insight not installed follow following steps
 - First goto inside the folder and open new_redis_host_dev.sh and uncomment the following code and save the file
```
Cmd - cd Modbus-Slave-Simulator
Cmd - sudo nano new_redis_host_dev.sh
```


- Text to uncomment -  

```
# If docker and docker compose is not installed please uncomment following lines
#echo "Installing Docker"
#curl -fsSL https://get.docker.com -o get-docker.sh
#sudo sh get-docker.sh
#sudo systemctl start docker
#echo "installing docker compose"
#sudo pip3 install docker compose
```

For saving the file press ctrl+x type y and hit enter

- Now run this bash file it will host docker containers it will take time please wait
```
Cmd - sudo bash nano new_redis_host_dev.sh
```

3) If Redis database newly setup first goto create_csv_add_data_redis folder and open create_redis_db_and_push_data.py file replace redis_ip value with your actual pc ip address and run this file it will automatically setup database 0.

```
Cmd - cd  create_csv_add_data_redis
Cmd - sudo nano create_redis_db_and_push_data.py
Text to edit -
    redis_ip = "192.168.1.219"  # change ip according to redis is hosted ip
```

For saving the file press ctrl+x type y and hit enter
```
Cmd - python3 create_redis_db_and_push_data.py
```


#### Note -  If not created virtual environment please create python virtual environment and activate it and then try to run code.
```
Cmd - python3 -m venv venv
Cmd - source venv/bin/activate
Cmd - python3 create_redis_db_and_push_data.py
```

4) Once the database successfully setup now we can run the simulator for the following steps.
- First go to Modbus-Slave-Simulator folder and open main file and change redis_ip
```
Cmd - cd Modbus-Slave-Simulator
Cmd - sudo nano main.py
Text to edit - 
	redis_ip = "192.168.1.219"  # change ip according to redis is hosted ip
```
For saving the file press ctrl+x type y and hit enter

- Now run the main file before running need to create python virtual environment and activate it then run main file
```
Cmd - python3 -m venv venv
Cmd - source venv/bin/activate
Cmd - python3 main.py
```

---
* * *
___

# Test the Modbus Slave Simulator:

1. First create modbus_slave_test folder goto inside the folder and create python virtual environment and activate it
```
Cmd - mkdir modbus_slave_test
Cmd - python3 -m venv venv
Cmd - source venv/bin/activate
```

2. Now install the pymodbus.console library for that run following command
```
Cmd - pip install ".[repl]"
Cmd - pip install "git+https://github.com/pymodbus-dev/repl"
```

3. Now connect to our simulator 
```
Cmd - pymodbus.console tcp --host <simulaor_pc_ip_address> --port 1505
```

4. Once connect through pymodbus we can do following operations using pymodbus inbuilt commands
##### a. Create connection
```
Cmd - client.connect
```
##### b. Read holding registers
```
Cmd - client.read_holding_registers address=1 count=5 unit=1
```
##### c. Write holding register or registers
##### i. For write single holding register 
```
Cmd - client.write_register address=1 value=7 unit=1
```
##### ii. For write multiple holding registers
```
Cmd - client.write_registers address=1 values=1,2,3 unit=1
```
##### d. Read coil registers
```
Cmd - client.read_coils address=1 count=8 unit=1
```
##### e. Write coil or coils
##### i. For write single coil register
```
Cmd - client.write_coil address=1 value=1 unit=1
```
##### ii. For write multiple coil registers
```
Cmd - client.write_coils address=1 values=1,1,1 unit=1
```
##### f. Read input registers
```
Cmd - client.read_input_registers address=1 count=5 unit=1
```
##### g. Read discrete input registers
```
Cmd - client.read_discrete_inputs address=1 count=5 unit=1
```
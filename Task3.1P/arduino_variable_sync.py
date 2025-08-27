import sys
import traceback
from arduino_iot_cloud import ArduinoCloudClient
import asyncio
import datetime
import csv
import os
import time

DEVICE_ID = "fd1a0a63-8a7a-4543-9772-45700c2bed83"
SECRET_KEY = "gUAP4qnzweFwKmnFfhXYTzLik"

# Open files for writing data
temp_file = open("randomTemperature.csv", "a")
humidity_file = open("humidity.csv", "a")

# Write headers if files are empty
if temp_file.tell() == 0:
    temp_file.write("time,value\n")
if humidity_file.tell() == 0:
    humidity_file.write("time,value\n")

# Callback function for temperature changes
def on_temperature_changed(client, value):
    print(f"New temperature: {value}")
    timestamp = datetime.datetime.now().isoformat() + "Z"
    csv_string = f"{timestamp},{value}\n"
    
    if temp_file:
        temp_file.write(csv_string)
        temp_file.flush()

# Callback function for humidity changes
def on_humidity_changed(client, value):
    print(f"New humidity: {value}")
    timestamp = datetime.datetime.now().isoformat() + "Z"
    csv_string = f"{timestamp},{value}\n"
    
    if humidity_file:
        humidity_file.write(csv_string)
        humidity_file.flush()

def main():
    print("Starting Arduino Cloud client...")

    # Instantiate Arduino cloud client
    client = ArduinoCloudClient(
        device_id=DEVICE_ID, username=DEVICE_ID, password=SECRET_KEY
    )

    # Register both temperature and humidity cloud variables
    client.register("temperature", value=None, on_write=on_temperature_changed)
    client.register("humidity", value=None, on_write=on_humidity_changed)

    # Start cloud client
    client.start()

if __name__ == "__main__":
    try:
        main()  # main function which runs in an internal infinite loop
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_tb(exc_type, exc_value, exc_traceback)
    finally:
        # Close files when done
        if temp_file:
            temp_file.close()
        if humidity_file:
            humidity_file.close()
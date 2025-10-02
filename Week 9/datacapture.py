import serial
import csv
import time


SERIAL_PORT = "COM7"
BAUD_RATE = 9600
CSV_FILE = "sensor_log.csv"

ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
time.sleep(2)  

with open(CSV_FILE, mode='w', newline='') as file:
    
    file.write("# Sensor Log File\n")
    file.write("# timestamp_ms = time since Arduino started (milliseconds)\n")
    file.write("# temperature_C = temperature from DHT22 (°C)\n")
    file.write("# humidity_percent = relative humidity from DHT22 (%)\n")
    file.write("# distance_cm = distance from HC-SR04 ultrasonic sensor (cm)\n")

    writer = csv.writer(file)
    
    writer.writerow(["timestamp_ms", "temperature_C", "humidity_percent", "distance_cm"])

    try:
        while True:
            line = ser.readline().decode('utf-8').strip()
            if line and not line.startswith("---") and not line.startswith("===") and not line.startswith("Error"):
                parts = line.split(",")
                if len(parts) == 4:
                    writer.writerow(parts)
                    file.flush()
                    print("Logged:", parts)
    except KeyboardInterrupt:
        print("Logging stopped by user.")
        ser.close()

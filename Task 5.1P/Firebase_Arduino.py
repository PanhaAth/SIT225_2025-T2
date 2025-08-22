import serial
import time
import json
from datetime import datetime, timezone
import firebase_admin
from firebase_admin import credentials, db

run_time = 30
COM_PORT = 'COM5'

run_time_seconds = run_time * 60
start_time = time.time()

cred = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://fir-real-414e3-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

ref = db.reference('/gyroscope_readings')

ser = serial.Serial(COM_PORT, 9600, timeout=1)
ser.flushInput()
print("Connected to Arduino")

try: 
    while True:
        line_bytes = ser.readline()
        try:
            line = line_bytes.decode('utf-8').strip()
        except UnicodeDecodeError:
            continue
        
        # Try comma-separated first, then tab-separated
        if line and (',' in line or '\t' in line):
            try:
                if ',' in line:
                    gx, gy, gz = map(float, line.split(','))
                else:
                    gx, gy, gz = map(float, line.split('\t'))
                
                timestamp = datetime.now(timezone.utc).isoformat()
                data_to_upload = {
                    'gyro_x': gx,
                    'gyro_y': gy,
                    'gyro_z': gz,
                    'timestamp': timestamp
                }
                new_ref = ref.push(data_to_upload)
                print(f"Data Uploaded: {data_to_upload}")
            except ValueError:
                print(f"Error parsing line: {line}")
                continue
        else: 
            print(f"Received line in wrong format: {line}")
except KeyboardInterrupt:
    print("\nStopped by user")
finally:
    ser.close()
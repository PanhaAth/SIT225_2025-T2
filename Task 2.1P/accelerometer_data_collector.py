import serial
import time
from datetime import datetime
import os

#configuration
SERIAL_PORT = 'COM5'
Baudrate = 9600
DATA_FOLDER = 'accelerometer_data'
Sampling_Rate = 50 # Hz

#Create data directory if it doeesn't exist
os.makedirs(DATA_FOLDER, exist_ok=True)
print(f"Current working directory: {os.getcwd()}")

def get_timestamp():
    return datetime.now().strftime("%Y%m%d%H%M%S")

def parse_accelerometer_data(line):
    """Parses the incoming accelerometer data from Arduino"""
    try:
        parts = line.strip().split(',')
        if len(parts) == 3:
            return [float(parts[0]), float(parts[1]), float(parts[2])]
        return None
    except Exception as e:
        print(f"Error parsing data: {e}")
        return None

def save_to_file(timestamp, data):
    """Saves data to CSV file"""
    filename = f"{DATA_FOLDER}/accelerometer_data.csv"
    with open(filename, 'a') as f:
        f.write(f"{timestamp},{','.join(map(str, data))}\n")

def main():
    print("Starting accelerometer data collection...")
    print(f"Sampling rate: {Sampling_Rate}Hz")

    try:
        ser = serial.Serial(SERIAL_PORT, Baudrate, timeout=1)
        time.sleep(2)  # wait for the serial connection to initialize

        start_time = time.time()
        collection_duration = 30 * 60

        print("Collecting data... Press Ctrl+C to stop early")

        while time.time() -start_time <collection_duration:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').strip()
                if line:
                    data = parse_accelerometer_data(line)
                    if data:
                        timestamp = get_timestamp()
                        save_to_file(timestamp, data)
                        
            time.sleep(1/Sampling_Rate - 0.002)

        print("Data collection complete.")

    except serial.SerialException as e:
        print(f"Serial connection error: {e}")
    except KeyboardInterrupt:
        print("Data collection interrupted by user.")
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()
    
if __name__ == "__main__":
    main()
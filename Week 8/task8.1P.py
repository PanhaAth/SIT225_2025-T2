import sys
import traceback
import csv
import os
from datetime import datetime
from arduino_iot_cloud import ArduinoCloudClient

DEVICE_ID = "f9be03ce-1809-4bf5-93c1-b3a4cc67a3e4"
SECRET_KEY = "7L4y@Ol4!jggkGIFrk2pKONxL"
COMBINED_FILE = "accel_combined.csv"

# Data buffer to store values until we have all three
data_buffer = {'x': None, 'y': None, 'z': None}
data_count = 0

def initialize_combined_file():
    """Initialize the combined CSV file with headers"""
    if not os.path.exists(COMBINED_FILE):
        with open(COMBINED_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['timestamp', 'x', 'y', 'z'])
        print(f"Created new combined CSV file: {COMBINED_FILE}")

def save_complete_dataset():
    """Save complete dataset to CSV when all three values are available"""
    global data_count
    
    if all(value is not None for value in data_buffer.values()):
        timestamp = datetime.now().isoformat()
        
        with open(COMBINED_FILE, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                timestamp,
                data_buffer['x'],
                data_buffer['y'],
                data_buffer['z']
            ])
        
        data_count += 1
        print(f"Dataset #{data_count}: {timestamp}, "
              f"x={data_buffer['x']:.3f}, "
              f"y={data_buffer['y']:.3f}, "
              f"z={data_buffer['z']:.3f}")
        
        # Reset buffer for next dataset
        data_buffer.update({'x': None, 'y': None, 'z': None})

# Callback functions
def on_x(client, value):
    data_buffer['x'] = value
    print(f"Received X: {value:.3f}")
    save_complete_dataset()

def on_y(client, value):
    data_buffer['y'] = value
    print(f"Received Y: {value:.3f}")
    save_complete_dataset()

def on_z(client, value):
    data_buffer['z'] = value
    print(f"Received Z: {value:.3f}")
    save_complete_dataset()

def main():
    print("=" * 60)
    print("ARDUINO CLOUD ACCELEROMETER DATA LOGGER - STEP 4")
    print("=" * 60)
    print("Saving COMBINED data to:", COMBINED_FILE)
    print("File format: <timestamp>, <x>, <y>, <z>")
    print("Data is saved only when all 3 values are received")
    print("Press Ctrl+C to stop the application")
    print("=" * 60)
    
    # Initialize the combined CSV file
    initialize_combined_file()
    
    try:
        # Create Arduino Cloud client
        client = ArduinoCloudClient(
            device_id=DEVICE_ID, 
            username=DEVICE_ID, 
            password=SECRET_KEY
        )

        # Register variables with callbacks
        client.register("py_x", value=None, on_write=on_x)
        client.register("py_y", value=None, on_write=on_y)
        client.register("py_z", value=None, on_write=on_z)
        
        # Start listening for data
        print("Listening for accelerometer data...")
        client.start()
        
    except KeyboardInterrupt:
        print("\n" + "=" * 60)
        print("Application stopped by user")
        print(f"Total complete datasets saved: {data_count}")
        print("=" * 60)
    except Exception as e:
        print(f"\nError: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main()
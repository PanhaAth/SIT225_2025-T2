# capture_gyro_data.py
import serial
import time
import csv

# Configure serial connection
SERIAL_PORT = 'COM5'  # Change to your Arduino's port
BAUD_RATE = 9600
OUTPUT_FILE = 'gyroscope_data.csv'

def capture_gyroscope_data():
    try:
        # Initialize serial connection
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        time.sleep(2)  # Wait for connection to establish
        
        # Open CSV file for writing
        with open(OUTPUT_FILE, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            
            # Write header (without activity)
            csv_writer.writerow(['timestamp', 'x', 'y', 'z'])
            
            print(f"Recording gyroscope data for 10 minutes...")
            print("Press Ctrl+C to stop early")
            
            start_time = time.time()
            end_time = start_time + (10 * 60)
            
            # Read data until time elapses
            while time.time() < end_time:
                if ser.in_waiting > 0:
                    line = ser.readline().decode('utf-8').strip()
                    
                    # Skip empty lines and header lines
                    if line and not any(header in line for header in 
                                       ['Gyroscope', 'X\tY\tZ', 'sample rate', 'timestamp,x,y,z']):
                        
                        # Parse the line - handle both CSV and tab-separated formats
                        if ',' in line:
                            parts = line.split(',')
                        else:
                            parts = line.split('\t')
                        
                        # We expect either 3 values (x,y,z) or 4 values (timestamp,x,y,z)
                        if len(parts) >= 3:
                            try:
                                # Handle different formats
                                if len(parts) == 3:
                                    # Only x,y,z values - use current time as timestamp
                                    timestamp = int(time.time() * 1000)
                                    x = float(parts[0])
                                    y = float(parts[1])
                                    z = float(parts[2])
                                else:
                                    # timestamp,x,y,z format
                                    timestamp = int(parts[0])
                                    x = float(parts[1])
                                    y = float(parts[2])
                                    z = float(parts[3])
                                
                                csv_writer.writerow([timestamp, x, y, z])
                                csvfile.flush()  # Ensure data is written immediately
                                
                                # Display progress
                                elapsed = time.time() - start_time
                                print(f"Elapsed: {elapsed:.1f}s, X: {x:.2f}, Y: {y:.2f}, Z: {z:.2f}")
                            except ValueError:
                                # Skip lines that can't be parsed
                                continue
                
                time.sleep(0.01)  # Small delay to prevent CPU overload
            
        print(f"Data collection complete. Saved to {OUTPUT_FILE}")
        
    except serial.SerialException as e:
        print(f"Serial connection error: {e}")
    except KeyboardInterrupt:
        print("\nData collection stopped by user")
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()

if __name__ == "__main__":
    capture_gyroscope_data()
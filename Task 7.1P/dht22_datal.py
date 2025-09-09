import serial
import time
from datetime import datetime
import os

# ---- Configuration ----
SERIAL_PORT   = 'COM5'       # e.g. 'COM5' on Windows, '/dev/ttyACM0' on macOS/Linux
BAUDRATE      = 9600
DURATION_MIN  = 35           # record for 35 minutes
DATA_FOLDER   = 'dht22_data'
OUTPUT_FILE   = os.path.join(DATA_FOLDER, 'dht22_data.csv')

# ---- Setup output ----
os.makedirs(DATA_FOLDER, exist_ok=True)

def write_header_if_new(path):
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        with open(path, 'w', encoding='utf-8') as f:
            f.write("timestamp,temperature_c,humidity_pct\n")

def parse_arduino_line(line: str):
    """
    Parses Arduino output like:
      'Time: 613s | Humidity: 49.80% | Temperature: 22.70°C'
    Returns (temp_c, humidity_pct) or None.
    """
    try:
        parts = [p.strip() for p in line.split('|')]
        if len(parts) != 3:
            return None

        hum_str = parts[1].split(':', 1)[1].replace('%', '').strip()
        temp_str = parts[2].split(':', 1)[1].replace('°C', '').replace('C', '').strip()

        h = float(hum_str)
        t = float(temp_str)
        return t, h
    except Exception:
        return None

def save_row(path, now_str, t, h):
    with open(path, 'a', encoding='utf-8') as f:
        f.write(f"{now_str},{t:.2f},{h:.2f}\n")

def main():
    print("Starting DHT22 data collection (using PC clock)...")
    print(f"Writing to: {os.path.abspath(OUTPUT_FILE)}")
    write_header_if_new(OUTPUT_FILE)

    try:
        ser = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=1)
        time.sleep(2.0)          # allow board reset
        ser.reset_input_buffer()

        end_time = time.monotonic() + DURATION_MIN * 60
        print(f"Collecting for {DURATION_MIN} minutes... (Ctrl+C to stop early)")

        while time.monotonic() < end_time:
            raw = ser.readline()
            if not raw:
                continue

            line = raw.decode('utf-8', errors='ignore').strip()
            if not line:
                continue

            parsed = parse_arduino_line(line)
            if parsed is None:
                continue

            t, h = parsed

            # Use current PC clock for timestamp
            now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            save_row(OUTPUT_FILE, now_str, t, h)
            print(f"{now_str} | {t:.2f} °C | {h:.2f} %")

        print("Data collection complete (35 minutes reached).")

    except serial.SerialException as e:
        print(f"Serial connection error: {e}")
        print("Tips: check COM port, close Arduino Serial Monitor, verify baud rate (9600).")
    except KeyboardInterrupt:
        print("Data collection interrupted by user.")
    finally:
        try:
            if 'ser' in locals() and ser.is_open:
                ser.close()
        except Exception:
            pass
        print("Serial port closed.")

if __name__ == "__main__":
    main()

import serial
import random
import time
from datetime import datetime

baud_rate = 9600

s = serial.Serial('COM5', baud_rate, timeout=5)

while True: #infinite loop, keep running

    #a random number between 1 and 10.
    data_send = random.randint(1, 10)
    d = s.write((str(data_send) + '\r\n').encode('utf-8'))
    print(f"[{datetime.now().strftime('%H:%M:%S')}] SEND >>> {data_send} ({d} bytes)")

    received_data = s.readline().decode("utf-8").strip()
    if received_data.isdigit():
        Sec = int(received_data)
        print(f"[{datetime.now().strftime('%H:%M:%S')}] RECV <<< {Sec} sleep for {Sec}s")
    #Sleep for the calculated time
    time.sleep(Sec)

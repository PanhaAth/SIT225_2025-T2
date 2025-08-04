import serial
import random
import time
from datetime import datetime

baud_rate = 9600

s = serial.Serial('COM5', baud_rate, timeout=5)

while True: #infinite loop, keep running

    #a random number between 9 and 50.
    data_send = random.randint(5, 50)
    d = s.write((str(data_send) + '\r\n').encode('utf-8'))
    print(f"[{datetime.now().strftime('%H:%M:%S')}] SEND >>> {data_send} ({d} bytes)")

    received_data = s.readline().decode("utf-8").strip()
    Sec = d/10 + 1
    print(f"[{datetime.now().strftime('%H:%M:%S')}] RECEIVE <<< {d} sleep for {Sec}s")

    #Sleep for the calculated time
    time.sleep(Sec)

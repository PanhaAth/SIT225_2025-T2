import firebase_admin
from firebase_admin import credentials, db
import pandas as pd

cred = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://fir-real-414e3-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

ref = db.reference('/gyroscope_readings')

all_data = ref.get()

if all_data is None:
    print("No data found in Firebase.")
    exit()
    
data_list = []
for firebase_key, reading in all_data.items():
    reading['firebase_key'] = firebase_key
    data_list.append(reading)

df = pd.DataFrame(data_list)
df['timestamp'] = pd.to_datetime(df['timestamp'])
df = df.sort_values('timestamp')

print("Missing values per column: ")
print(df.isnull().sum())

df[['gyro_x', 'gyro_y', 'gyro_z']] = df[['gyro_x', 'gyro_y', 'gyro_z']].apply(pd.to_numeric, errors='coerce')

df_clean = df.dropna(subset = ['gyro_x', 'gyro_y', 'gyro_z'])
print(f"Removed {len(df) - len(df_clean)} rows with invalid data.")

csv_filename = "gyroscrope_readings.csv"
df_clean.to_csv(csv_filename, index=False)
print("Clean data saved to {csv_filename}")
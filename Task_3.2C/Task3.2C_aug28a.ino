#include "arduino_secrets.h"
#include "thingProperties.h"
#include <ArduinoIoTCloud.h>
#include <DHT.h>
#include<Arduino_ConnectionHandler.h>

#define DHTPIN 2
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);

//Define the temperature threshold
const float TEMP_HIGH_THRESHOLD = 25.0;
const float TEMP_LOW_THRESHOLD = 15.0;

void setup() {
  // Initialize serial and wait for port to open:
  Serial.begin(9600);
  // This delay gives the chance to wait for a Serial Monitor without blocking if none is found
  delay(1500); 

  dht.begin();

  // Defined in thingProperties.h
  initProperties();

  // Connect to Arduino IoT Cloud
  ArduinoCloud.begin(ArduinoIoTPreferredConnection);
  
  /*
     The following function allows you to obtain more information
     related to the state of network and IoT Cloud connection and errors
     the higher number the more granular information you’ll get.
     The default is 0 (only errors).
     Maximum is 4
 */
  setDebugMessageLevel(2);
  ArduinoCloud.printDebugInfo();

  alarm_message = "System Normal";
}

void loop() {
  ArduinoCloud.update();
  
  float newTemperature = dht.readTemperature();
  float newHumidity = dht.readHumidity();

  if (isnan(newTemperature) || isnan(newHumidity))
  {
    Serial.println(F("Failed to read from DHT sensor!"));
    delay(1000);
    return;
  }

  temperature = newTemperature;
  humidity = newHumidity;

  Serial.print("Temperature: ");
  Serial.print(temperature);
  Serial.println(" C");
  Serial.print("Humidity: ");
  Serial.println(humidity);
  Serial.print("Alarm: ");
  Serial.println(alarm_status ? "ON" : "OFF");

  if(!alarm_status) {
    if (temperature > TEMP_HIGH_THRESHOLD)
    {
      alarm_status = true;
      alarm_message = "HIGH TEMP ALARM! > " + String(TEMP_HIGH_THRESHOLD) + "C";
    }
    else if (temperature < TEMP_LOW_THRESHOLD){
    alarm_status = true;
    alarm_message = "LOW TEMP ALARM! < " + String(TEMP_LOW_THRESHOLD) + "C";
    }
  }
  
  delay(5000);
  
}

/*
  Since Temperature is READ_WRITE variable, onTemperatureChange() is
  executed every time a new value is received from IoT Cloud.
*/
void onTemperatureChange()  {
  // Add your code here to act upon Temperature change
}

/*
  Since Humidity is READ_WRITE variable, onHumidityChange() is
  executed every time a new value is received from IoT Cloud.
*/
void onHumidityChange()  {
  // Add your code here to act upon Humidity change
}

/*
  Since AlarmStatus is READ_WRITE variable, onAlarmStatusChange() is
  executed every time a new value is received from IoT Cloud.
*/
void onAlarmStatusChange()  {
  if (!alarm_status) 
  {
    alarm_message = "System Normal";
    Serial.println("Alarm manually reset from dashboard");
  }
}

/*
  Since AlarmMessage is READ_WRITE variable, onAlarmMessageChange() is
  executed every time a new value is received from IoT Cloud.
*/
void onAlarmMessageChange()  {
  Serial.println("AlarmMessage updated from Cloud: " + alarm_message);
}
#include "arduino_secrets.h"
#include "thingProperties.h"
#include <Adafruit_Sensor.h>
#include <DHT.h>
#include <DHT_U.h>

#define DHTPIN 2
#define DHTTYPE DHT22

DHT_Unified dht(DHTPIN, DHTTYPE);
unsigned long lastUpdate = 0;
const long interval = 2000; // Update every 2 seconds

// Implement the callback functions - FIXED THE TYPO HERE
void onRandomTemperatureChange() { // Changed "Chang1e" to "Change"
  // This function will be called when random_Temperature is changed from the cloud
  Serial.print("Temperature changed from cloud: ");
  Serial.println(randomTemperature);
}

void onHumidityChange() {
  // This function will be called when humidity is changed from the cloud
  Serial.print("Humidity changed from cloud: ");
  Serial.println(humidity);
}

void readSensors() {
  sensors_event_t event;
  
  // Read temperature from DHT22
  dht.temperature().getEvent(&event);
  if (isnan(event.temperature)) {
    Serial.println("Error reading temperature!");
  } else {
    randomTemperature = event.temperature; // Update cloud variable
    Serial.print("Temperature: ");
    Serial.print(randomTemperature);
    Serial.println(" °C");
  }
  
  // Read humidity from DHT22
  dht.humidity().getEvent(&event);
  if (isnan(event.relative_humidity)) {
    Serial.println("Error reading humidity!");
  } else {
    humidity = event.relative_humidity; // Update cloud variable
    Serial.print("Humidity: ");
    Serial.print(humidity);
    Serial.println(" %");
  }
}

void setup() {
  Serial.begin(9600);
  while (!Serial); // Wait for serial port to connect
  
  dht.begin();
  
  initProperties();
  ArduinoCloud.begin(ArduinoIoTPreferredConnection);
  setDebugMessageLevel(2);
  ArduinoCloud.printDebugInfo();

  Serial.println("Setup complete");
}

void loop() {
  ArduinoCloud.update(); // Keep the cloud connection alive

  // Use non-blocking timer instead of delay()
  unsigned long currentMillis = millis();
  if (currentMillis - lastUpdate >= interval) {
    lastUpdate = currentMillis;
    readSensors(); // Call the function to read sensors and update variables
  }
}
#include "DHT.h"

#define DHTPIN 2
#define DHTTYPE DHT22

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  Serial.println(F("DHT22 Temperature and Humidity Monitor"));
  dht.begin();
}

void loop() {
  // Wait between measurements (changed to 1000ms as requested)
  delay(1000);

  // Reading temperature or humidity takes about 250 milliseconds!
  float h = dht.readHumidity();
  float t = dht.readTemperature();

  // Check if any reads failed and exit early (to try again).
  if (isnan(h) || isnan(t)) {
    Serial.println(F("Failed to read from DHT sensor!"));
    return;
  }

  // Print timestamp (millis since start)
  Serial.print(F("Time: "));
  Serial.print(millis() / 1000);
  Serial.print(F("s | "));
  
  // Print humidity and temperature
  Serial.print(F("Humidity: "));
  Serial.print(h);
  Serial.print(F("% | Temperature: "));
  Serial.print(t);
  Serial.println(F("°C"));
}
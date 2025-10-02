#include "DHT.h"

#define DHTPIN 2        
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);

#define TRIG_PIN 3      
#define ECHO_PIN 4      

long duration;
float distance;

void setup() {
  Serial.begin(9600);
  dht.begin();

  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);

  Serial.println("=== Smart Indoor Safety & Comfort Monitor ===");
  Serial.println("timestamp_ms,temp_C,humidity_percent,distance_cm"); // CSV header
}

void loop() {

  float temp = dht.readTemperature();
  float humidity = dht.readHumidity();

  if (isnan(temp) || isnan(humidity)) {
    Serial.println("Error: DHT22 read failed");
    return;
  }

 
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  duration = pulseIn(ECHO_PIN, HIGH);
  distance = duration * 0.034 / 2;  // cm

  Serial.println("----------------------------");
  Serial.print("Timestamp (ms): ");
  Serial.println(millis());
  Serial.print("Temperature: ");
  Serial.print(temp);
  Serial.println(" °C");
  Serial.print("Humidity: ");
  Serial.print(humidity);
  Serial.println(" %");
  Serial.print("Distance: ");
  Serial.print(distance);
  Serial.println(" cm");

  // --- CSV output (single line) ---
  Serial.print(millis());
  Serial.print(",");
  Serial.print(temp);
  Serial.print(",");
  Serial.print(humidity);
  Serial.print(",");
  Serial.println(distance);

  delay(2000); // capture every 2 seconds
}

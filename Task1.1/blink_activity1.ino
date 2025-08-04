int receivedNumber;

void setup() {
  Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);
  while (!Serial);  // Wait for serial connection
  randomSeed(analogRead(0));  // Initialize random number generator
}

void loop() {
  if (Serial.available()) {
    // Step 1: Receive number from Python
    receivedNumber = Serial.parseInt();
    Serial.read();  // Clear the newline character
    
    // Step 2: Blink LED with 1-second interval
    for (int i = 0; i < receivedNumber; i++) {
      digitalWrite(LED_BUILTIN, HIGH);
      delay(500);  // On for 0.5s
      digitalWrite(LED_BUILTIN, LOW);
      delay(500);  // Off for 0.5s (total 1s interval)
    }
    
    // Step 3: Send random number back to Python
    int randomNum = random(5, 50);  // Range 5-50
    Serial.println(randomNum);
  }
}

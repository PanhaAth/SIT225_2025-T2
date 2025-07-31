int x;

void setup() {
  // put your setup code here, to run once:
Serial.begin(9600);
pinMode(LED_BUILTIN, OUTPUT);
while(!Serial);
}

void loop() {
  // put your main code here, to run repeatedly:
x = Serial.readString().toInt();
Serial.println(x);
for(int i = 0; i < x; i++)
{
  digitalWrite(LED_BUILTIN, HIGH);
  delay(100);
  digitalWrite(LED_BUILTIN, LOW);
  delay(100);
}

Serial.flush();
delay(1000);
}

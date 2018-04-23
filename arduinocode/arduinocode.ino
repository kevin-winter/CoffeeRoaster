int temp1_pin = 0;
int led_pin = 13;

int led = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(led_pin, OUTPUT);
}

void loop() {
  write();
  read();
  delay(1000);
}

void write(){
  Serial.println(analogRead(temp1_pin));
}

void read() {
  if(Serial.available() > 0) {
    led = Serial.read();
    if(led > 0)
      digitalWrite(led_pin, HIGH);
    else
      digitalWrite(led_pin, LOW);
  }
  
}


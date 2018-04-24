#include <Servo.h>

Servo moter1;

int temp1_pin = 1;
int led_pin = 13;
int led = 0;

double r = 0;
double t = 0;


void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(led_pin, OUTPUT);
  //moter1.attach(3);
}

void loop() {
  write();
  read();
  delay(500);
}

void motor() {
  moter1.write(30);
  delay(1000);
  moter1.write(120);
}

void write(){
  r = 10000.0/((1023.0/analogRead(1))-1.0);
  t = (1 / ( log(r/100000)/3950 + 1.0/(20+273.15)) - 273.15);
  Serial.println(t);
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


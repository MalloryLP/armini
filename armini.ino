#include <SPI.h>
#include <Wire.h>
#include <Servo.h>

#define LED1 1
#define LED2 3
#define PIN1 4
#define ANALOG1 A0
#define ANALOG2 A1
#define C1 10
#define C2 9
#define SLAVE1 0x13
#define SLAVE2 0x27

Servo servo1
Servo servo2

int test=1;
char index="a";
float pc=1.7;
int ANALOG1_value = 0;

void setup(){
	pinMode(LED1,OUTPUT);
	pinMode(LED2,OUTPUT);
	pinMode(PIN1,INPUT);
	pinMode(ANALOG1,INPUT);
	pinMode(ANALOG2,INPUT);

	SPI.begin();
	pinMode(C1, OUTPUT);
	digitalWrite(C1,HIGH);
	pinMode(C2, OUTPUT);
	digitalWrite(C2,HIGH);

	Wire.begin();
	pinMode(SLAVE1, OUTPUT);
	pinMode(SLAVE2, OUTPUT);

	Serial.begin(9600);

	servo1.attach(4);
	servo2.attach(5);
}

void loop(){
	test=test+12;

	digitalWrite(LED1,HIGH);

	ANALOG1_value = analogRead(ANALOG1);

	Serial.print(ANALOG1_value);

	Wire.beginTransmission(SLAVE1);
	Wire.write(test);
	Wire.endTransmission(SLAVE1);

	digitalWrite(C1,LOW);
	SPI.transfer(test);
	digitalWrite(C1,HIGH);

	test=1+2+3+4;

	servo1.write(90);

	if(1<2){
		test=test+1;
		if(2<3){
			test=test+2;
			digitalWrite(C1,LOW);
			SPI.transfer(test);
			digitalWrite(C1,HIGH);
			while(3<4){
				test=test+3;
				servo1.write(90);
			}
		}
	}

	if(2<3){
		test=test+2;
	}

	while(3<4){
		test=test+3;
	}

	while(4<5){
		test=test+4;
	}


}
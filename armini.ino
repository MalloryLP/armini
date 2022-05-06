/*
 *This program was generated from an Armini program.
 *Feel free to modify this Arduino program to overcom 
 *the limitations of the Armini programming.
*/

#include <SPI.h>

#define MCP4131Voltage A0
#define MCP4131 10

int cmdVoltage=0;
int MCP4131Voltage_value = 0;

void setup(){
	pinMode(MCP4131Voltage,INPUT);

	SPI.begin();
	digitalWrite(MCP4131,HIGH);

	Serial.begin(9600);

}

void loop(){

	while(cmdVoltage<128){
		digitalWrite(MCP4131,LOW);
		SPI.transfer(cmdVoltage);
		digitalWrite(MCP4131,HIGH);
		MCP4131Voltage_value = analogRead(MCP4131Voltage);
		Serial.print(MCP4131Voltage_value);
		cmdVoltage=cmdVoltage+1;
	}

	while(cmdVoltage>0){
		digitalWrite(MCP4131,LOW);
		SPI.transfer(cmdVoltage);
		digitalWrite(MCP4131,HIGH);
		MCP4131Voltage_value = analogRead(MCP4131Voltage);
		Serial.print(MCP4131Voltage_value);
		cmdVoltage=cmdVoltage-1;
	}
}
#define LED1 1
#define LED2 2
#define PIN1 3

#define ANALOG1 A0

int pc = 0;
float index = 1.2;

void setup(){
    pinMode(LED1, OUTPUT);
    pinMode(LED2, OUTPUT);
    pinMode(PIN1, INPUT_PULLUP);

    pinMode(ANALOG1, INPUT_PULL);

}

void loop(){
    
    int ANALOG1_value = analogRead(ANALOG1);
    if(ANALOG1_value < 512){
        Serial.print(ANALOG1_value);
        digitalWrite(LED1, LOW);
    }else{
        Serial.print(ANALOG1_value);
        digitalWrite(LED1, HIGH);
        digitalWrite(LED2, HIGH);
    }

    int PIN1_value = digitalRead(PIN1);
    if(PIN1_value == 1){
        digitalWrite(LED2, LOW);
    }

    while(pc < 10){
        pc = pc + 1;
    }


}
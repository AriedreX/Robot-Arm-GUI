/*****************************************
* Robot Arm Control Program with Arduino *
* created by Antonio Galiza              *
* 22/09/2019                             *
******************************************/
#include <Servo.h>

Servo servo0;
Servo servo1;
Servo servo2;
Servo servo3;

int servo0Pin = 5;
int servo1Pin = 6;
int servo2Pin = 9;
int servo3Pin = 10;
int servoAngles[4]={0,90,90,90};

void setup() {
    servo0.attach(servo0Pin);
    servo1.attach(servo1Pin);
    servo2.attach(servo2Pin);
    servo3.attach(servo3Pin);
    // initialize serial communication at 9600 bits per second:
    Serial.begin(9600);
    while(!Serial);
    Serial.print("Initialized\n");
    pinMode(LED_BUILTIN, OUTPUT);
}
void loop() {
    //if some date is sent, reads it and saves in state
     char line[16]={'0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','\0'};
     int counter0=0;
          
     while(Serial.available()){
      delay(3);
      if (Serial.available()>0){
        line[counter0] = Serial.read();
        counter0++;
      }
    }
    line[16]='\0';
     servo0.write(servoAngles[0]);
     delay(15);
     servo1.write(servoAngles[1]);
     delay(15);
     servo2.write(servoAngles[2]);
     delay(15);
     servo3.write(servoAngles[3]);
    delay(100);
     if (line[15]=='a') {
            Serial.println(line);
            int counter1 = 0;
            int pos_comma = 0;
            while (counter1<=4){
              int counter2 = 0;
              char num[4]={'0','0','0','\0'};
              while(counter2<4){
                if (line[pos_comma+counter2]!=','){
                  num[counter2]=line[pos_comma+counter2];
                  counter2++;
                }else{
                  counter2++;
                  pos_comma = pos_comma+counter2;
                  counter2++;
                  break;
                }                            
              }
              servoAngles[counter1] = atoi(num);
              counter1++; 
            }
           
          }
}

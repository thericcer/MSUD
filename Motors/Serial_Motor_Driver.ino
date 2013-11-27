/*
 * Serial motor controller
 * Recieves a serial string formatted as such-
 *   M, SL, SR, DirL, DirR
 *   M, A1, A2, A3, A4 
 * The first byte corresponds to what motor set we are controlling, Steering or Drive.
 * The next four bytes correspond to the speed/direction or angle at which to run/turn the motor. 
 * 
 * Finally the code checks the validty of the string, then sets the appropriate pins
 * to drive the called for motors.
 * 
 * Upon further thinking on steering, the 2 front and 2 rear motors can not be tied
 * to eachother because that would make steering impossible. We must independantly 
 * control each motor seperately.
 *
 * Oct 21 2013
 * Ric Clark
 */

#include <Servo.h>

#define DRIVE 'D'
#define STEER 'S'
#define FORWARD 'F'
#define SENSOR 'Z'

char MotorString[5];

/* Define a Status Byte, This will be sent as a response to recieving a 5 byte command packet
 * 
 * 0                       7
 * |B0|B1|B2|B3|B4|B5|B6|B7|
 *
 * B0 - If Set, Motors were Killed by External Interrupt, Action Needs to be taken
 * B1 - Command Received, Values changed
 * More to come
 */
char StatusByte = 0;
char LoopCount = 0;

int SensorArray[4] = {0};

Servo leftFront;
Servo leftRear;
Servo rightFront;
Servo rightRear;
char newData;

void setup(){
  //Begin Serial at common baud rate.
  Serial.begin(9600);
  
  /*Setup Drive Motor pins, assuming motors 1 and 2 are
    are the right motors. Pin 2 and 3
    are connected to either side of the H-Bridge. A HIGH 
    value on Pin 2 and LOW value on Pin 3 will drive them
    both forward. Same setup for the left motors on pins 
    4 and 5.
  */
  pinMode(2, OUTPUT);
  pinMode(3, OUTPUT);
  pinMode(4, OUTPUT);
  pinMode(5, OUTPUT);
  
  digitalWrite(2, LOW);
  digitalWrite(3, LOW);
  digitalWrite(4, LOW);
  digitalWrite(5, LOW);
  
  /*Setup Drive Motor speed. The pins that the H-Bridge enable
    pins are tied to need to be PWM pins. Using the analog
    write function of the Arduino we can vary the speed of the 
    motors from 0 to Full On using a PWM signal with a duty cycle
    determined by the value written to the pin. The value ranges 
    from 0 to 255. 0 meaning no output and 255 being full on. The 
    pins capable of doing this are 5 and 6.
  */
  pinMode(6, OUTPUT);
  pinMode(11, OUTPUT);
  
  //Attach Servos and set initial angle
  leftFront.attach(7);
  leftRear.attach(8);
  rightFront.attach(9);
  rightRear.attach(10);
  
  leftFront.write(0);
  leftRear.write(0);
  rightFront.write(0);
  rightRear.write(0);
}

void loop(){
  newData = 0;
  //Serial.println("Hello");
  //Loop until we get 5 bytes from the UART then read them into MotorString
  if(Serial.available() == 5){
    newData = 1;
    for(int i = 0; i < 5 ; i++){
      MotorString[i] = Serial.read();
    }
    StatusByte = 0x02 | StatusByte; 
    Serial.write(StatusByte);
    
  }
  if (newData){
    //Figure out what motors are called for
    switch (MotorString[0]){
      
      //Drive motors called
      case DRIVE: 
      
        //Set Direction, Assuming we want both front and back going the same way
        if (MotorString[3] == FORWARD){
          digitalWrite(2, HIGH);
          digitalWrite(3, LOW);
          
        }
        else {
          digitalWrite(2, LOW);
          digitalWrite(3, HIGH);
          
        }
        
        if (MotorString[4] == FORWARD){
          digitalWrite(4, HIGH);
          digitalWrite(5, LOW);
        }
        
        else {
          digitalWrite(4, LOW);
          digitalWrite(5, HIGH);
        }
        
        
        //Next set speed
        analogWrite(6, MotorString[1]);
        analogWrite(11, MotorString[2]);
        //Serial.print(" Speed L: ");
        //Serial.print(MotorString[1], DEC);
        //Serial.print(" R: ");
        //Serial.println(MotorString[2], DEC);
        break;
        
      case STEER:
      
        //Check and set servo angles
        if(MotorString[1] <= 180){
            leftFront.write(MotorString[1]);
        }
        
        if(MotorString[2] <= 180){
            leftRear.write(MotorString[2]);
        }
        
        if(MotorString[3] <= 180){
            rightFront.write(MotorString[3]);
        }
        
        if(MotorString[4] <= 180){
            rightRear.write(MotorString[4]);
        }
                
        break;
        
        
      case SENSOR:
        Serial.write(SensorArray[MotorString[1]] & 0xFF);
        Serial.write((SensorArray[MotorString[1]] >> 8) & 0xFF);
        break;
        
      default:
        break;
    }
  }
  
  
  //Update Sensor Values.
  if(LoopCount == 1){
    SensorArray[0] = analogRead(0);
  }
  if(LoopCount == 2){
    //SensorArray[1] = 15;
    pinMode(12, OUTPUT);
    digitalWrite(12, LOW);
    delayMicroseconds(2);
    digitalWrite(12, HIGH);
    delayMicroseconds(5);
    digitalWrite(12, LOW);
    pinMode(12, INPUT);    
    SensorArray[1] = (pulseIn(12, HIGH)/29)/2;
    
    //Serial.println(SensorArray[1], DEC);
    LoopCount = 0;
  }
  
  LoopCount++;
}
  



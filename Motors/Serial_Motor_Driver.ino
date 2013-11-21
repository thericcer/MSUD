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

#define DRIVE 0x44
#define STEER 0x53
#define FORWARD 0x46

char MotorString[5];

Servo leftFront;
Servo leftRear;
Servo rightFront;
Servo rightRear;

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
  pinMode(10, OUTPUT);
  pinMode(11, OUTPUT);
  
  //Attach Servos and set initial angle
  leftFront.attach(6);
  leftRear.attach(7);
  rightFront.attach(8);
  rightRear.attach(9);
  
  leftFront.write(0);
  leftRear.write(0);
  rightFront.write(0);
  rightRear.write(0);
}

void loop(){
  //Serial.println("Hello");
  //Loop until we get 5 bytes from the UART then read them into MotorString
  if(Serial.available() == 5){
    //Serial.println("In if");
    for(int i = 0; i < 5 ; i++){
      MotorString[i] = Serial.read();
    }
    
  }
  
  //Figure out what motors are called for
  switch (MotorString[0]){
    
    //Drive motors called
    case DRIVE: 
    
      //Set Direction, Assuming we want both front and back going the same way
      if (MotorString[3] == FORWARD){
        digitalWrite(2, HIGH);
        digitalWrite(3, LOW);
        digitalWrite(4, HIGH);
        digitalWrite(5, LOW);
        Serial.print("Drive Motors Set Forward");
        
      }
      else {
        digitalWrite(2, LOW);
        digitalWrite(3, HIGH);
        digitalWrite(4, LOW);
        digitalWrite(5, HIGH);
        Serial.print("Drive Motors Set Reverse");
      }
      
      //Next set speed
      analogWrite(10, MotorString[1]);
      analogWrite(11, MotorString[2]);
      Serial.print(" Speed L: ");
      Serial.print(MotorString[1], DEC);
      Serial.print(" R: ");
      Serial.println(MotorString[2], DEC);
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
      
      Serial.print("Steer Motors set to angles: ");
      Serial.print(MotorString[1]);
      Serial.print(MotorString[2]);
      Serial.print(MotorString[3]);
      Serial.println(MotorString[4]);
              
      break;
      
    default:
      break;
  }
  
}
  



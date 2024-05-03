#include <Servo.h>

Servo myServo; // Create a servo object
int currentAngle = 145; // Variable to track the current angle
int targetAngle = 90; // Target angle to rotate to
int increment = 5; // Angle increment for each step
int delayTime = 1000; // Delay time in milliseconds

void setup() {
  myServo.attach(7); // Attach the servo to pin 7
}

void loop() {
  while (currentAngle != targetAngle) {
    if (currentAngle < targetAngle) {
      currentAngle += increment; // Increment the current angle
    } else {
      currentAngle -= increment; // Decrement the current angle
    }
    myServo.write(currentAngle); // Set the servo position
    delay(delayTime); // Wait for the servo to reach the position
  }
  delay(5000);

  while (currentAngle != 145) { // Assuming 145 is the original angle
    if (currentAngle < 145) {
      currentAngle += increment; // Increment the current angle
    } else {
      currentAngle -= increment; // Decrement the current angle
    }
    myServo.write(currentAngle); // Set the servo position
    delay(delayTime); // Wait for the servo to reach the position
  }
}
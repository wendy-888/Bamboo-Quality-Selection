#include <Servo.h>
#include <ezButton.h>
#include <Wire.h>
#include "Adafruit_AS726x.h"

//button
ezButton limitSwitch(7); // create ezButton object that attaches to pin 7
bool buttonPressed = false;

//motor
Servo myServo; // Create a servo object
int totalAngle = 0;

//collision
const int trigPin = 9;
const int echoPin = 10;
long duration;
float distance;

//colour
Adafruit_AS726x ams;
uint16_t sensorValues[AS726x_NUM_CHANNELS];

// Function prototypes
void rotateMotor();
void detectCollision();
void measureColor();

void setup() {
  //collision
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  
  Serial.begin(9600);
  limitSwitch.setDebounceTime(50);

  //colour
  while (!Serial);
  pinMode(LED_BUILTIN, OUTPUT);
  if (!ams.begin()) {
    Serial.println("Could not connect to sensor! Please check your wiring.");
    while (1);
  }
}

int buttonPressCount = 0;

void loop() {
  buttonPressed = checkButton();

  if (buttonPressed) {
    buttonPressed = false;
    buttonPressCount = 0;
    detectCollision();
    delay(50); // debounce delay
  } else {
    if (buttonPressCount < 2) {
      measureColor();
      buttonPressCount++;
    }
  }

  if (buttonPressCount >= 2) {
    while (!buttonPressed) {
      buttonPressed = checkButton();
    }
  }

  delay(1000);
}

bool checkButton() {
  limitSwitch.loop();
  return limitSwitch.isPressed();
}

void detectCollision() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  duration = pulseIn(echoPin, HIGH);
  distance = duration * 0.034 / 2;
  Serial.print("D");
  Serial.println(distance);
}

void measureColor() {
  uint8_t temp = ams.readTemperature();
  ams.startMeasurement();
  bool ready = false;
  while (!ready) {
    ready = ams.dataReady();
  }
  ams.readRawValues(sensorValues);
  uint8_t red = map(sensorValues[AS726x_RED], 0, 255, 0, 255);
  uint8_t green = map(sensorValues[AS726x_GREEN], 0, 255, 0, 255);
  uint8_t blue = map(sensorValues[AS726x_BLUE], 0, 255, 0, 255);
  Serial.print("R");
  Serial.println(red);
  Serial.print("G");
  Serial.println(green);
  Serial.print("B");
  Serial.println(blue);
  delay(500);
}
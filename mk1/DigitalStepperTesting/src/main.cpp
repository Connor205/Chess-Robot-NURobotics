#include <Arduino.h>

const int stepPin = 3;
const int dirPin = 2;

void setup()
{
    // put your setup code here, to run once:
    pinMode(stepPin, OUTPUT);
    pinMode(dirPin, OUTPUT);
    pinMode(LED_BUILTIN, OUTPUT);
    Serial.begin(9600);
}

void loop()
{
    digitalWrite(dirPin, LOW);
    for (int i = 0; i < 1600; i++) {
        // turn on the step pin
        digitalWrite(stepPin, HIGH);
        // wait for a bit
        delayMicroseconds(100);
        // turn off the step pin
        digitalWrite(stepPin, LOW);
        // wait for a bit
        delayMicroseconds(100);
    }
    digitalWrite(dirPin, HIGH);
    for (int i = 0; i < 1600; i++) {
        // turn on the step pin
        digitalWrite(stepPin, HIGH);
        // wait for a bit
        delayMicroseconds(100);
        // turn off the step pin
        digitalWrite(stepPin, LOW);
        // wait for a bit
        delayMicroseconds(100);
    }
    digitalWrite(LED_BUILTIN, HIGH);
    delay(1000);
    digitalWrite(LED_BUILTIN, LOW);
    Serial.println("Hello World!");
}
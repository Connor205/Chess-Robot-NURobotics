#include <Arduino.h>
#include <CustomAxis.h>
#include <Utils.h>

const int stepPinX = 2;
const int dirPinX = 5;

const int stepPinZ = 4;
const int dirPinZ = 7;

const int stepPinY = 3;
const int dirPinY = 6;

int yAxisStepPins[] = { stepPinX, stepPinZ };
int yAxisDirPins[] = { dirPinX, dirPinZ };
bool yAxisForwardDirs[] = { true, false };
CustomAxis yAxis = CustomAxis(yAxisStepPins, yAxisDirPins, yAxisForwardDirs, "yAxis");

CustomAxis axes[] = { yAxis };

int numAxes = sizeof(axes) / sizeof(CustomAxis);

void setup()
{
    Serial.begin(9600);
    Serial.flush();
    digitalWrite(8, LOW);
    writeInfo("Running Setup");
    // Init all axes in the array
    for (int i = 0; i < numAxes; i++) {
        // We call init here so that we can monitor the serial output
        axes[i].init();
        // Here we also go ahead and calibrate the axis, if the axis has no limit switch, nothing will happen. We are
        // not doing any enforcing of calibration her
        axes[i].calibrateAxis();
    }
    writeInfo("Setup Complete");
}

void basicMovement()
{
    yAxis.moveTo(100);
    yAxis.moveTo(0);
    yAxis.moveToAccel(100);
    yAxis.moveToAccel(0);
    delay(1000);
}

void moveBasedOnSerial()
{
    // Wait for an input from the serial port
    waitForSerialInput();
    // Read the input
    String input = Serial.readStringUntil('\n');
    // Check if string is equal to yAxis
    if (input.equals("yAxis")) {
        // Read integer from Serial
        int targetStep = Serial.parseInt();
        // Move the axis to the target step
        yAxis.moveTo(targetStep);
    } else {
        writeError("Unknown command: " + input);
    }
}

void loop()
{
    // Here our loop is pretty much just a placeholder
    // We can call whatever function we are testing at the moment here
    moveBasedOnSerial();
}

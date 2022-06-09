#include <Arduino.h>
#include <CustomAxis.h>
#include <Servo.h>
#include <Utils.h>

// X YL YR Z
// Direction, step
const int dirPinX = 2;
const int stepPinX = 3;
const int xLimitSwitchPin = 49;

const int dirPinYL = 4;
const int stepPinYL = 5;

const int dirPinYR = 6;
const int stepPinYR = 7;

const int yLimitSwitchPin = 48;

const int dirPinZ = 8;
const int stepPinZ = 9;

const int zLimitSwitchPin = 50;

int yAxisStepPins[] = { stepPinYL, stepPinYR };
int yAxisDirPins[] = { dirPinYL, dirPinYR };
bool yAxisForwardDirs[] = { true, false };
int xAxisStepPins[] = { stepPinX };
int xAxisDirPins[] = { dirPinX };
bool xAxisForwardDirections[] = { true };
int zAxisStepPins[] = { stepPinZ };
int zAxisDirPins[] = { dirPinZ };
bool zAxisForwardDirections[] = { false };

CustomAxis yAxis = CustomAxis(yAxisStepPins, yAxisDirPins, yAxisForwardDirs, "yAxis", 2, yLimitSwitchPin, false);
CustomAxis xAxis = CustomAxis(xAxisStepPins, xAxisDirPins, xAxisForwardDirections, "xAxis", 1, xLimitSwitchPin, false);
CustomAxis zAxis = CustomAxis(zAxisStepPins, zAxisDirPins, zAxisForwardDirections, "zAxis", 1, zLimitSwitchPin, true);

CustomAxis axes[] = { yAxis, xAxis, zAxis };

int numAxes = sizeof(axes) / sizeof(CustomAxis);
Servo leftGrabber;
Servo rightGrabber;

void grab()
{
    leftGrabber.write(177);
    rightGrabber.write(3);
    delay(1000);
}
void ungrab()
{
    leftGrabber.write(168);
    rightGrabber.write(12);
    delay(1000);
}
void raise() { zAxis.moveToAccel(473); }
void lowerToBoard() { zAxis.moveToAccel(3973); }
void lowerToTaken() { zAxis.moveToAccel(4300); };

void smallRaise() { zAxis.moveToAccel(3873); }
void smallPickup()
{
    lowerToBoard();
    grab();
    smallRaise();
}

void setup()
{
    Serial.begin(9600);
    Serial.flush();
    digitalWrite(8, LOW);
    writeState("startup");
    writeInfo("Running Setup");
    writeInfo("Attaching Servos");
    leftGrabber.attach(30);
    rightGrabber.attach(31);
    grab();
    ungrab();
    grab();

    yAxis.init();
    xAxis.init();
    zAxis.init();

    writeState("calibrating");
    zAxis.calibrateAxis();

    yAxis.calibrateAxis();
    lowerToBoard();
    xAxis.calibrateAxis();
    raise();
    ungrab();
    writeInfo("Setup Complete");
}

void basicMovement()
{
    yAxis.moveToAccel(2000);
    delay(1000);
    yAxis.moveToAccel(0);
    delay(1000);
    xAxis.moveToAccel(2000);
    delay(1000);
    xAxis.moveToAccel(0);
    delay(1000);
    yAxis.moveToAccel(0);
}

void moveBasedOnSerial()
{
    // Wait for an input from the serial port
    waitForSerialInput();
    // Read the input
    String input = Serial.readStringUntil('\n');
    writeInfo("Received: " + input);
    // Check if string is equal to yAxis
    if (input.equals("yAxis")) {
        waitForSerialInput();
        // Read integer from Serial
        int targetStep = Serial.parseInt();
        // Move the axis to the target step
        yAxis.moveToAccel(targetStep);
    } else if (input.equals("xAxis")) {
        waitForSerialInput();
        // Read integer from Serial
        int targetStep = Serial.parseInt();
        // Move the axis to the target step
        xAxis.moveToAccel(targetStep);

    } else {
        writeError("Unknown command: " + input);
    }
}

void asyncMovement()
{
    xAxis.setTarget(2000);
    yAxis.setTarget(2000);
    while (xAxis.isMoving() || yAxis.isMoving()) {
        xAxis.update();
        yAxis.update();
    }
    xAxis.setTarget(0);
    yAxis.setTarget(0);
    while (xAxis.isMoving() || yAxis.isMoving()) {
        xAxis.update();
        yAxis.update();
    }
}

void zAxisMovement()
{
    zAxis.moveToAccel(800);
    delay(1000);
    zAxis.moveToAccel(0);
    delay(1000);
    zAxis.moveToAccel(1600);
    delay(1000);
    zAxis.moveToAccel(0);
    delay(1000);
    zAxis.moveToAccel(0);
}
void xAxisMovement()
{
    xAxis.moveToAccel(1000);
    delay(1000);
    xAxis.moveToAccel(0);
    delay(1000);
}

void servoMovement()
{
    grab();
    raise();
    xAxis.setTarget(1000);
    yAxis.setTarget(1000);
    while (xAxis.isMoving() || yAxis.isMoving()) {
        xAxis.update();
        yAxis.update();
    }
    lowerToBoard();
    ungrab();
    grab();
    raise();
    xAxis.setTarget(0);
    yAxis.setTarget(0);
    while (xAxis.isMoving() || yAxis.isMoving()) {
        xAxis.update();
        yAxis.update();
    }
    lowerToBoard();
    ungrab();
}

void testMMMovement()
{
    grab();
    xAxis.setRelativeMM(40 * 7);
    xAxis.waitToStop();
    delay(5000);
    xAxis.setRelativeMM(-40 * 7);
    xAxis.waitToStop();
    delay(5000);
}

void waitForXY()
{
    while (xAxis.isMoving() || yAxis.isMoving()) {
        xAxis.update();
        yAxis.update();
    }
}

void lowerGrabReturn()
{
    lowerToBoard();
    ungrab();
    grab();
    raise();
}

void dropPiece()
{
    lowerToBoard();
    ungrab();
    raise();
}
void pickUpPiece()
{
    lowerToBoard();
    grab();
    raise();
}
void dropTakenPiece()
{
    lowerToTaken();
    ungrab();
    raise();
}

void pickUpTakenPiece()
{
    lowerToTaken();
    grab();
    raise();
}

void movePieces()
{
    yAxis.setRelativeMM(97);
    // Starting h8
    for (int i = 0; i < 7; i++) {
        ungrab();
        raise();
        xAxis.setRelativeMM(40 * 7);
        yAxis.setRelativeMM(40);
        waitForXY();
        pickUpPiece();
        xAxis.setRelativeMM(-40 * 7);
        waitForXY();
        dropPiece();
    }
    while (true) {
        delay(1000);
    }
}

void testLimit()
{
    pinMode(xLimitSwitchPin, INPUT_PULLUP);
    Serial.println(digitalRead(xLimitSwitchPin));
    delay(500);
}

void firstSquareCalibration()
{
    yAxis.setTarget(953);
    xAxis.setTarget(648);
    waitForXY();
}

const int yAxisOffset = 922;
const int xAxisOffset = 616;

void goToSquare(int x, int y)
{
    // Check if square is less than 0 or greater than 7
    // if it is return
    if (x < 0 || x > 7 || y < 0 || y > 7) {
        writeError("Square is out of bounds");
        return;
    }
    // 0,0 is top left or a8
    // 7,7 is bottom right or h1

    long ySteps = convertMMToSteps(40 * y);
    long xSteps = convertMMToSteps(40 * x);
    yAxis.setTarget(yAxisOffset + ySteps);
    xAxis.setTarget(xAxisOffset + xSteps);
    waitForXY();
}
const int leftBlackTakenX = 67;
const int rightBlackTakenX = 3982;
const int topBlackTakenY = 970;
void moveToBlackTaken(int x, int y)
{
    if ((x != -1 && x != 1) || y < 0 || y > 7) {
        writeError("Square is out of bounds");
        return;
    }
    long xTarget = 0;
    if (x == -1) {
        xTarget = leftBlackTakenX;
    } else if (x == 1) {
        xTarget = rightBlackTakenX;
    }
    long yTarget = topBlackTakenY + convertMMToSteps(y * 40);
    yAxis.setTarget(yTarget);
    xAxis.setTarget(xTarget);
    waitForXY();
}

const int upperLeftWhiteTakenX = 190;
const int upperLeftWhiteTakenY = 20;
const int xGap = convertMMToSteps(90);

void moveToWhiteTaken(int x, int y)
{
    if (x < 0 || x > 7 || y < 0 || y > 1) {
        writeError("Square is out of bounds");
        return;
    }
    long xTarget = upperLeftWhiteTakenX + convertMMToSteps(x * 40);
    if (x > 3) {
        xTarget += xGap;
    }
    long yTarget = upperLeftWhiteTakenY + convertMMToSteps(y * 40);
    yAxis.setTarget(yTarget);
    xAxis.setTarget(xTarget);
    waitForXY();
}

void getRidOfPiece()
{
    goToSquare(0, 0);
    yAxis.setRelativeMM(-60);
    waitForXY();
    ungrab();
    goToSquare(0, 0);
}

void testSquares()
{
    goToSquare(0, 0);
    delay(1000);
    goToSquare(7, 7);
    delay(1000);
    goToSquare(0, 7);
    delay(1000);
    goToSquare(7, 0);
    delay(1000);
}

void moveToSquareSerial()
{
    writeState("ready");
    // Wait for an input from the serial port
    waitForSerialInput();
    // Read the input
    String input = Serial.readStringUntil('\n');
    writeInfo("Received - " + input);
    writeState("moving");
    // Check if string is equal to yAxis
    if (input.equals("pickup")) {
        pickUpPiece();
    } else if (input.equals("pickupTaken")) {
        pickUpTakenPiece();
    } else if (input.equals("drop")) {
        dropPiece();
    } else if (input.equals("dropTaken")) {
        dropTakenPiece();
    } else if (input.equals("lowerToBoard")) {
        lowerToBoard();
    } else if (input.equals("lowerToTaken")) {
        lowerToTaken();
    } else if (input.equals("raise")) {
        raise();
    } else if (input.equals("smallPickup")) {
        smallPickup();
    } else if (input.equals("grab")) {
        grab();
    } else if (input.equals("ungrab")) {
        ungrab();
    } else if (input.equals("remove")) {
        getRidOfPiece();
    } else if (input.equals("move")) {
        int x = Serial.parseInt();
        waitForSerialInput();
        // Read integer from Serial
        int y = Serial.parseInt();
        goToSquare(x, y);
    } else if (input.equals("moveBlackTaken")) {
        int x = Serial.parseInt();
        waitForSerialInput();
        // Read integer from Serial
        int y = Serial.parseInt();
        moveToBlackTaken(x, y);
    } else if (input.equals("moveWhiteTaken")) {
        int x = Serial.parseInt();
        waitForSerialInput();
        // Read integer from Serial
        int y = Serial.parseInt();

        moveToWhiteTaken(x, y);
    } else if (input.equals("home")) {
        xAxis.setTarget(100);
        yAxis.setTarget(100);
        waitForXY();
        writeState("home");
    } else {
        writeError("Invalid Command");
    }
}

void loop() { moveToSquareSerial(); }

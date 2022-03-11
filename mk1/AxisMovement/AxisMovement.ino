/*X.STEP is connected with the Arduino’s pin number 2.
  Y.STEP is connected with the Arduino’s pin number 3.
  Z.STEP is connected with the Arduino’s pin number 4.
  X.DIR is connected with the Arduino’s pin number 5
  Y.DIR is connected with the Arduino’s pin number 6
  Z.DIR is connected with the Arduino’s pin number 7
*/

const int stepPinX = 2;
const int dirPinX = 5;

const int stepPinZ = 4;
const int dirPinZ = 7;

const int stepPinY = 3;
const int dirPinY = 6;

class CustomStepper {
  private:
    int dirPin;
    int stepPin;
    int currentStep;
    int target;
    bool currentDirection;

  public:
    CustomStepper(int dirPinInput, int stepPinInput)
    {
      this->dirPin = dirPinInput;
      this->stepPin = stepPinInput;
      init();
    }

    void init()
    {
      pinMode(dirPin, OUTPUT);
      pinMode(stepPin, OUTPUT);
      resetStepCount();
      setDirection(true);
    }

    int getDirPin() {
      return dirPin;
    }

    int getStepPin() {
      return stepPin;
    }

    void resetStepCount() {
      currentStep = 0;
    }

    void setDirection(bool forward)
    {
      if (forward) {
        digitalWrite(dirPin, HIGH);
        currentDirection = true;
      } else {
        digitalWrite(dirPin, LOW);
        currentDirection = false;
      }
    }

    bool getDirection() {
      return currentDirection;
    }

    void moveTo(int targetStep)
    {
      if (currentStep > targetStep) {
        setDirection(false);
      }

      int stepsToMake = abs(targetStep - currentStep);
      for (int i = 0; i < stepsToMake; i++) {
        digitalWrite(stepPin, HIGH);
        delayMicroseconds(500);
        digitalWrite(stepPin, LOW);
        delayMicroseconds(500);
      }
      currentStep = targetStep;
    }

    void moveAbsolute(int numSteps)
    {
      if (numSteps < 0) {
        setDirection(false);
      } else {
        setDirection(true);
      }

      int stepsToMake = abs(numSteps);
      for (int i = 0; i < stepsToMake; i++) {
        digitalWrite(stepPin, HIGH);
        delayMicroseconds(500);
        digitalWrite(stepPin, LOW);
        delayMicroseconds(500);
      }
      currentStep = currentStep + numSteps;
    }

    void setTarget(int target) {
      target = target;
    }
};

int getDelayFromSpeed(int s) {
  // Here we are converting ticks per second into a delay timing
  double period = 1.0 / s;
  return period * 1000000;
}



class CustomAxis {
  private:
    int* stepPins;
    int* dirPins;
    bool* forwardDirections;
    int numMotors;
    bool currentDirection;
    int current;
    int target;
    int mSpeed; // max speed in ticks per second
    int cSpeed;
    int cDelay;

  public:
    CustomAxis(int stepPins_[], int dirPins_[], bool forwardDirections_[])
    {
      stepPins = stepPins_;
      dirPins = dirPins_;
      forwardDirections = forwardDirections_;
      init();
    }

    void init()
    {
      // Lets grab some of the inital values we care about
      current = 0;
      target = 0;
      mSpeed = 4000;
      cSpeed = 2000;
      cDelay = getDelayFromSpeed(cSpeed);
      numMotors = sizeof(stepPins) / sizeof(int) + 1;

      for (int i = 0; i < numMotors; i++) {
        // Lets set up the pins for the motors
        pinMode(stepPins[i], OUTPUT);
        pinMode(dirPins[i], OUTPUT);
      }
    }

    bool* getDirections() {
      return forwardDirections;
    }

    int getNumMotors() {
      return numMotors;
    }

    void setSpeed(int s) {
      // Speed is given in steps per second
      cSpeed = s;
      cDelay = getDelayFromSpeed(s);
    }

    // Sets the direction based on a boolean, if the boolean is true, the motor will move forward, if false, it will
    // move backward
    void setDirection(bool dir)
    {
      if (dir) {
        for (int i = 0; i < numMotors; i++) {
          if (forwardDirections[i]) {
            digitalWrite(dirPins[i], HIGH);
          }
          else {
            digitalWrite(dirPins[i], LOW);
          }
        }
      }
      else {
        for (int i = 0; i < numMotors; i++) {
          if (forwardDirections[i]) {
            digitalWrite(dirPins[i], LOW);
          }
          else {
            digitalWrite(dirPins[i], HIGH);
          }
        }
      }
      currentDirection = !currentDirection;
    }

    void writeAllMotors(bool high)
    {
      for (int i = 0; i < numMotors; i++) {
        if (high) {
          digitalWrite(stepPins[i], HIGH);
        } else {
          digitalWrite(stepPins[i], LOW);
        }
      }
    }

    void stepAllMotors()
    {
      writeAllMotors(true);
      delayMicroseconds(cDelay);
      writeAllMotors(false);
      delayMicroseconds(cDelay);
    }

    void moveTo(int targetStep)
    {
      // We can go ahead and set the direction of the motors
      if (current > targetStep) {
        setDirection(false);
      } else {
        setDirection(true);
      }
      delay(100);


      int stepsToMake = abs(targetStep - current);
      Serial.println(stepsToMake);
      for (int i = 0; i < stepsToMake; i++) {
        stepAllMotors();
      };
      current = targetStep;
    }
    
    int getQuadraticSpeedCurve(int currentStep, int totalSteps) {
      // Lets start with a simple quadratic expression
      // minSpeed at 0, minSpeed at totalSteps and maxSpeed at currentStep
      int minSpeed = 400;
      // Serial.println(mSpeed - ((4 * (mSpeed - minSpeed)) / (totalSteps ^ 2) * (currentStep - (totalSteps / 2)) ^ 2));
      return mSpeed - ((4 * (mSpeed - minSpeed)) / (totalSteps ^ 2) * (currentStep - (totalSteps / 2)) ^ 2);
    }

    int linearSpeedCurve(int currentStep, int totalSteps) {
      int diffFromMiddle = abs(currentStep - totalSteps / 2);
      double currentStepDouble = currentStep;
      double minSpeed = 800.0;
      return mSpeed - ((mSpeed - minSpeed) / (totalSteps / 2) * diffFromMiddle);
    }

    void moveToAccel(int targetStep) {
      // Here we want to do the same thing as move, but we want to accelerate and decelerate the axis over the number of steps
      // This involves turning our percentage completion into a speed
      // Then turning that speed into a delay timing

      // We can go ahead and set the direction of the motors
      if (current > targetStep) {
        setDirection(false);
      } else {
        setDirection(true);
      }

      int stepsToMake = abs(targetStep - current);
      for (int i = 0; i < stepsToMake; i++) {
        setSpeed(linearSpeedCurve(i, stepsToMake));
        stepAllMotors();
      };
      current = targetStep;
    }
};


int yAxisStepPins[] = {stepPinX, stepPinZ};
int yAxisDirPins[] = {dirPinX, dirPinZ};
bool yAxisForwardDirs[] = {true, false};

CustomAxis yAxis = CustomAxis(yAxisStepPins, yAxisDirPins, yAxisForwardDirs);


void setup()
{
  Serial.begin(9600);
  pinMode(8, OUTPUT);
}

void loop()
{
  digitalWrite(8, LOW);
  yAxis.moveToAccel(500);
//  yAxis.moveToAccel(800);
//  yAxis.moveToAccel(1000);
//  yAxis.moveToAccel(800);
//  yAxis.moveToAccel(1200);
  yAxis.moveToAccel(0);
  delay(1000);
}

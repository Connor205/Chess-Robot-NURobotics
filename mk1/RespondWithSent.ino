void setup() { Serial.begin(9600); }

void loop()
{
    if (Serial.available() > 0) {
        input1 = Serial.readStringUntil('\n');
        Serial.write("ACK:" + input1);
    }
}
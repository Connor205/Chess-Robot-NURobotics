void setup() { Serial.begin(9600); }
String input;
void loop()
{
    if (Serial.available() > 0) {
        input = Serial.readStringUntil('\n');
        Serial.println("ACK: " + input);
    }
}
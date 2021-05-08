void setup()
{
    pinMode(8, INPUT_PULLUP);
    pinMode(9, OUTPUT);
}

void loop()
{
    if (digitalRead(8) == LOW)
    {
        digitalWrite(9, HIGH);
    }
    else
    {
        digitalWrite(9, LOW);
    }
}
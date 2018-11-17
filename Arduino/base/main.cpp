#include <Arduino.h>

void setup() {
  init();
  Serial.begin(9600);

  pinMode(13, OUTPUT);
}

int main() {
  setup();

  while (true) {
    digitalWrite(13, HIGH);
    delay(1000);
    digitalWrite(13, LOW);
    delay(1000);
  }
}

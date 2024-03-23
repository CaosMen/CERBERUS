#include "Arduino.h"

#include "include/person_detection.h"

bool personDetection(tflite::ErrorReporter* error_reporter, int8_t person_score, int8_t person_threshold) {
  static bool is_initialized = false;
  if (!is_initialized) {
    /* Pins for the built-in RGB LEDs on the Arduino Nano 33 BLE Sense */
    pinMode(LEDR, OUTPUT);
    pinMode(LEDG, OUTPUT);
    pinMode(LEDB, OUTPUT);

    is_initialized = true;
  }

  /* Turn off all LEDs */
  digitalWrite(LEDR, HIGH);
  digitalWrite(LEDG, HIGH);
  digitalWrite(LEDB, HIGH);
  
  /* Flash the blue LED after every inference */
  digitalWrite(LEDB, LOW);
  delay(100);
  digitalWrite(LEDB, HIGH);
  
  /* If the person score is greater than the no person score, turn on the red LED, else turn on the green LED */
  if (person_score > person_threshold) {
    digitalWrite(LEDR, HIGH);
    digitalWrite(LEDG, LOW);
    digitalWrite(LEDB, HIGH);
  } else {
    digitalWrite(LEDR, LOW);
    digitalWrite(LEDG, HIGH);
    digitalWrite(LEDB, HIGH);
  }

  /* Wait for a few seconds */
  delay(1000);

  /* Turn off all LEDs */
  digitalWrite(LEDR, HIGH);
  digitalWrite(LEDG, HIGH);
  digitalWrite(LEDB, HIGH);

  return person_score > person_threshold;
}

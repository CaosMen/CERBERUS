#include "Arduino.h"

#include <TinyMLShield.h>

#include "include/model_settings.h"
#include "include/image_provider.h"
#include "include/device_settings.h"

TfLiteStatus getImage(tflite::ErrorReporter* error_reporter, byte* image) {
  static bool g_is_camera_initialized = false;

  /* Initialize camera if necessary */
  if (!g_is_camera_initialized) {
    pinMode(LEDR, OUTPUT);
    pinMode(LEDG, OUTPUT);
    pinMode(LEDB, OUTPUT);

    if (!Camera.begin(QCIF, GRAYSCALE, 5, OV7675)) {
      TF_LITE_REPORT_ERROR(error_reporter, "[ERROR] Failed to initialize camera!");

      return kTfLiteError;
    }

    g_is_camera_initialized = true;
  }

  /* Turn off all LEDs */
  digitalWrite(LEDR, HIGH);
  digitalWrite(LEDG, HIGH);
  digitalWrite(LEDB, HIGH);

  /* The camera data is read and stored in the image array. */
  Camera.readFrame(image);

  /* Flash the green LED to confirm image capture */
  digitalWrite(LEDG, LOW);
  delay(200);
  digitalWrite(LEDG, HIGH);

  return kTfLiteOk;
}

TfLiteStatus getImageForModel(tflite::ErrorReporter* error_reporter, byte* image, int8_t* image_input) {
  static bool g_is_camera_initialized = false;

  /* Initialize camera if necessary */
  if (!g_is_camera_initialized) {
    if (!Camera.begin(QCIF, GRAYSCALE, 5, OV7675)) {
      TF_LITE_REPORT_ERROR(error_reporter, "[ERROR] Failed to initialize camera!");

      return kTfLiteError;
    }

    g_is_camera_initialized = true;
  }

  /* The camera data is read and stored in the image array. */
  Camera.readFrame(image);

  int index = 0;

  int min_x = (kCameraWidth - kNumRows) / 2;
  int min_y = (kCameraHeight - kNumCols) / 2;

  /* Crop 96x96 image. This lowers FOV, ideally we would downsample but this is simpler */
  for (int y = min_y; y < min_y + kNumCols; y++) {
    for (int x = min_x; x < min_x + kNumRows; x++) {
      /* Convert TF input image to signed 8-bit */
      image_input[index++] = static_cast<int8_t>(image[(y * kCameraWidth) + x] - 128);
    }
  }

  return kTfLiteOk;
}
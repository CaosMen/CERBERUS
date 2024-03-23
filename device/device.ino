#include <TensorFlowLite.h>

#include "include/image_provider.h"
#include "include/model_settings.h"
#include "include/device_settings.h"
#include "include/person_detection.h"
#include "include/person_detect_model_data.h"

#include "tensorflow/lite/version.h"
#include "tensorflow/lite/schema/schema_generated.h"
#include "tensorflow/lite/micro/micro_interpreter.h"
#include "tensorflow/lite/micro/micro_error_reporter.h"
#include "tensorflow/lite/micro/micro_mutable_op_resolver.h"

namespace {
  tflite::ErrorReporter* error_reporter = nullptr;
  const tflite::Model* model = nullptr;
  
  tflite::MicroInterpreter* interpreter = nullptr;
  TfLiteTensor* input = nullptr;

  constexpr int kTensorArenaSize = 136 * 1024;
  static uint8_t tensor_arena[kTensorArenaSize];
}

byte image[kCameraMaxImageSize];

void setup() {
  /* Set up the error reporter */
  static tflite::MicroErrorReporter micro_error_reporter;
  error_reporter = &micro_error_reporter;
  
  /* Get the tflite model */
  model = tflite::GetModel(g_person_detect_model_data);

  /* Check if the model version is valid */
  if (model->version() != TFLITE_SCHEMA_VERSION) {
    TF_LITE_REPORT_ERROR(
      error_reporter,
      "[ERROR] Model provided is schema version %d not equal to supported version %d.",
      model->version(), TFLITE_SCHEMA_VERSION
    );

    return;
  }

  /* Initialize the resolver */
  static tflite::MicroMutableOpResolver<5> micro_op_resolver;

  /* Add the operations to the resolver */
  micro_op_resolver.AddAveragePool2D();
  micro_op_resolver.AddConv2D();
  micro_op_resolver.AddDepthwiseConv2D();
  micro_op_resolver.AddReshape();
  micro_op_resolver.AddSoftmax();

  /* Build the interpreter to run the model with */
  static tflite::MicroInterpreter static_interpreter(model, micro_op_resolver, tensor_arena, kTensorArenaSize, error_reporter);
  interpreter = &static_interpreter;

  /* Aloocate the memory for the tensor flow arena */
  TfLiteStatus allocate_status = interpreter->AllocateTensors();

  /* Check if the allocation was successful */
  if (allocate_status != kTfLiteOk) {
    TF_LITE_REPORT_ERROR(error_reporter, "[ERROR] Failed to allocate tensors!");
    return;
  }

  /* Get information about the memory area to use for the model's input */
  input = interpreter->input(0);
}

void loop() {
  String command = "";
  bool isCommand = false;

  while (Serial.available()) {
    char c = Serial.read();
    if ((c != '\n') && (c != '\r')) {
      command.concat(c);
    } else if (c == '\r') {
      isCommand = true;
      command.toLowerCase();
    }
  }

  if (!isCommand) {
    return;
  }

  if (command == "capture") {
    isCommand = false;

    /* Get image from OV7675 camera */
    if (kTfLiteOk != getImage(error_reporter, image)) {
      TF_LITE_REPORT_ERROR(error_reporter, "[ERROR] Image capture failed.");
    }
    
    /* Send the captured image to the client encoded in HEX */
    for (int i = 0; i < kCameraMaxImageSize; i += 1) {
      Serial.print("0x");
      Serial.print(image[i], HEX);

      if (i < kCameraMaxImageSize - 1) {
        Serial.print(",");
      }
    }

    Serial.println();
  } else if (command == "capture-person") {
    isCommand = false;
    time_t start_time = millis();

    /* Capture the image until a person is detected */
    bool has_person = false;
    while (!has_person) {
      /* Check if the time has elapsed */
      if ((millis() - start_time) > (kMaxCaptureTime * 1000)) {
        TF_LITE_REPORT_ERROR(error_reporter, "[ERROR] Capture time exceeded.");
        break;
      }

      /* Get image from OV7675 camera */
      if (kTfLiteOk != getImageForModel(error_reporter, image, input->data.int8)) {
        TF_LITE_REPORT_ERROR(error_reporter, "[ERROR] Image capture failed.");
      }

      /* Run the model on this input */
      if (kTfLiteOk != interpreter->Invoke()) {
        TF_LITE_REPORT_ERROR(error_reporter, "[ERROR] Invoke failed.");
      }

      /* Get the output from the model */
      TfLiteTensor* output = interpreter->output(0);

      /* Get the person score from the output */
      int8_t person_score = output->data.uint8[kPersonIndex];
      
      bool person_detected = personDetection(error_reporter, person_score, kPersonThreshold);

      if (person_detected) {
        has_person = true;

        /* Send the captured image to the client encoded in HEX */
        for (int i = 0; i < kCameraMaxImageSize; i += 1) {
          Serial.print("0x");
          Serial.print(image[i], HEX);

          if (i < kCameraMaxImageSize - 1) {
            Serial.print(",");
          }
        }

        Serial.println();
      }
    }
  } else {
    TF_LITE_REPORT_ERROR(error_reporter, "[ERROR] Command not recognized.");
  }
}
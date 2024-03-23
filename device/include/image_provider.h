#ifndef IMAGE_PROVIDER_H_
#define IMAGE_PROVIDER_H_

#include "tensorflow/lite/c/common.h"
#include "tensorflow/lite/micro/micro_error_reporter.h"

/**
 * Function to get the image from the camera and store it in the image_data array.
 * 
 * @param error_reporter Error reporter object to report any errors.
 * @param image Array to store the image data.
 * 
 * @return Returns kTfLiteOk if the image was successfully captured and stored in the image_data array. 
 */
TfLiteStatus getImage(tflite::ErrorReporter* error_reporter, byte* image);

/**
 * Function to get the image from the camera and store it in the image_data array.
 * 
 * @param error_reporter Error reporter object to report any errors.
 * @param image Array to store the image data.
 * @param image_input Array to store the image data in the format required by the model.
 * 
 * @return Returns kTfLiteOk if the image was successfully captured and stored in the image_data array. 
 */
TfLiteStatus getImageForModel(tflite::ErrorReporter* error_reporter, byte* image, int8_t* image_input);

#endif // IMAGE_PROVIDER_H_

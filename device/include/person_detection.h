#ifndef PERSON_DETECTION_H_
#define PERSON_DETECTION_H_

#include "tensorflow/lite/c/common.h"
#include "tensorflow/lite/micro/micro_error_reporter.h"

/**
 * Function to respond to the detection of a person or no person.
 * 
 * @param error_reporter Error reporter object to report any errors.
 * @param person_score Score of the person class.
 * @param person_threshold Threshold for the person class.
 * 
 * @return Returns a boolean value indicating if image contains a person or not.
 */
bool personDetection(tflite::ErrorReporter* error_reporter, int8_t person_score, int8_t person_threshold);

#endif // PERSON_DETECTION_H_

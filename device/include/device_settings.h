#ifndef DEVICE_SETTINGS_H_
#define DEVICE_SETTINGS_H_

constexpr int kCameraWidth = 176;
constexpr int kCameraHeight = 144;
constexpr int kCameraChannels = 1;

constexpr int kCameraMaxImageSize = kCameraWidth * kCameraHeight * kCameraChannels;

constexpr int kPersonThreshold = 40;

constexpr int kMaxCaptureTime = 10;

#endif // DEVICE_SETTINGS_H_

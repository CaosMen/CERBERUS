#ifndef MODEL_SETTINGS_H_
#define MODEL_SETTINGS_H_

constexpr int kNumCols = 96;
constexpr int kNumRows = 96;
constexpr int kNumChannels = 1;

constexpr int kMaxImageSize = kNumCols * kNumRows * kNumChannels;

constexpr int kCategoryCount = 2;
constexpr int kPersonIndex = 1;
constexpr int kNotAPersonIndex = 0;

#endif  // MODEL_SETTINGS_H_

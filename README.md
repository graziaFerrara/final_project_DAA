### Problem 1: Part of Speech Tagging

One of the critical operations in speech recognition involves part-of-speech (POS) tagging. This process assigns roles to each part of a sentence (e.g., noun, verb, modal). Given transition and emission probabilities, we aim to determine the most likely sequence of roles for a given sentence.

#### Function `pos_tagging(R, S, T, E)`

- **Input:**
  - `R`: Tuple of roles.
  - `S`: Tuple of strings representing words in the sentence.
  - `T`: Dictionary representing transition probabilities between roles.
  - `E`: Dictionary representing emission probabilities between words and roles.

- **Output:**
  - Dictionary mapping words to assigned roles.

### Problem 2: Device Selection

In this problem, we need to select a subset of speech recognition devices for further testing. The goal is to choose a subset such that each device either dominates or is dominated by another device in the same subset.

#### Class `DeviceSelection`

- **Constructor `DeviceSelection(N, X, data)`**
  - `N`: Tuple of strings identifying the devices.
  - `X`: Integer representing the maximum sentence length.
  - `data`: Dictionary mapping devices to performance data.

- **Method `countDevices()`**
  - Returns the minimum number of devices needed for testing.

- **Method `nextDevice(i)`**
  - Input: Integer `i` representing the subset index.
  - Returns the next device to test within the specified subset.

These two problems address critical aspects of speech recognition testing and optimization, offering efficient solutions for practical implementation.

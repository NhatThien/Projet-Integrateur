import numpy as np

data = np.load("data/test_RGB_0_10_25.npy")
label = np.load("data/test_labels_0_10_25.npy")

np.save("test_mini_RGB.npy", data[:3])
np.save("test_mini_labels.npy", label[:3])
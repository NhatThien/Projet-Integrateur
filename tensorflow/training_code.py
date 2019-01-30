import tensorflow as tf;
from tensorflow import keras;
import numpy as np;
import matplotlib.pyplot as plt;

train_labels = np.load("../data/train_labels_0_10_25.npy")
train_images = np.load("../data/train_RGB_0_10_25.npy")
test_labels = np.load("../data/mini/test_lab.npy")
test_images = np.load("../data/mini/test_mini.npy")

class_name = ['forest', 'sea', 'city', 'mountain', 'plan']
class_index = [0, 1, 2, 3, 4]

train_labels = np.sum(train_labels*class_index, axis = 1)
test_labels = np.sum(test_labels*class_index, axis = 1)

model = keras.Sequential([
    keras.layers.Flatten(input_shape=(32, 32, 3)),
    keras.layers.Dense(1000, activation=tf.nn.relu),
    keras.layers.Dense(5, activation=tf.nn.softmax)
])

model.compile(optimizer=tf.train.AdamOptimizer(), 
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

model.fit(train_images, train_labels, epochs = 5)
test_loss, test_acc = model.evaluate(test_images, test_labels)
print('Test loss, test accuracy:', test_loss, test_acc)

predictions = model.predict(test_images)
print(predictions[0])
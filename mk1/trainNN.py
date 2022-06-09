import tensorflow as tf
from keras import layers
from keras.models import Sequential
import matplotlib.pyplot as plt

import pathlib

print("Finished Importing")

data_dir = pathlib.Path("training-data")

batch_size = 32
img_height = 120
img_width = 120

train_ds = tf.keras.utils.image_dataset_from_directory(data_dir,
                                                       validation_split=0.2,
                                                       subset="training",
                                                       seed=123,
                                                       image_size=(img_height,
                                                                   img_width),
                                                       batch_size=batch_size)
val_ds = tf.keras.utils.image_dataset_from_directory(data_dir,
                                                     validation_split=0.2,
                                                     subset="validation",
                                                     seed=123,
                                                     image_size=(img_height,
                                                                 img_width),
                                                     batch_size=batch_size)

num_classes = 3

model = Sequential([
    layers.Rescaling(1. / 255, input_shape=(img_height, img_width, 3)),
    layers.Conv2D(16,
                  3,
                  input_shape=(None, 120, 120, 3),
                  padding='same',
                  activation='relu'),
    layers.MaxPooling2D(),
    layers.Conv2D(32, 3, padding='same', activation='relu'),
    layers.MaxPooling2D(),
    layers.Conv2D(64, 3, padding='same', activation='relu'),
    layers.MaxPooling2D(),
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dense(num_classes)
])
model.compile(
    optimizer='adam',
    loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
    metrics=['accuracy'])
model.summary()

epochs = 20
history = model.fit(train_ds, validation_data=val_ds, epochs=epochs)
# Save model to file
model.save('model.h5')

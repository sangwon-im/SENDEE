import numpy as np
import argparse
import matplotlib.pyplot as plt
import cv2
from tensorflow.keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import BatchNormalization
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping
import os
import pickle
import time
from contextlib import redirect_stdout
import model as md

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

from tensorflow.python.client import device_lib
print(device_lib.list_local_devices())


# plots accuracy and loss curves
def plot_model_history(model_history):
    """
    Plot Accuracy and Loss curves given the model_history
    """
    fig, axs = plt.subplots(1,2,figsize=(15,5))
    # summarize history for accuracy
    axs[0].plot(range(1,len(model_history.history['accuracy'])+1),model_history.history['accuracy'])
    axs[0].plot(range(1,len(model_history.history['val_accuracy'])+1),model_history.history['val_accuracy'])
    axs[0].set_title('Model Accuracy')
    axs[0].set_ylabel('Accuracy')
    axs[0].set_xlabel('Epoch')
#     axs[0].set_xticks(np.arange(1,len(model_history.history['accuracy'])+1),len(model_history.history['accuracy'])/10)
    axs[0].legend(['train', 'val'], loc='best')
    # summarize history for loss
    axs[1].plot(range(1,len(model_history.history['loss'])+1),model_history.history['loss'])
    axs[1].plot(range(1,len(model_history.history['val_loss'])+1),model_history.history['val_loss'])
    axs[1].set_title('Model Loss')
    axs[1].set_ylabel('Loss')
    axs[1].set_xlabel('Epoch')
#     axs[1].set_xticks(np.arange(1,len(model_history.history['loss'])+1),len(model_history.history['loss'])/10)
    axs[1].legend(['train', 'val'], loc='best')
    fig.savefig(f'models/{nowtime}_log.png')



# If you want to train the same model or try other models, go for this
# model = Sequential()

# model.add(Conv2D(64, kernel_size=(3, 3), activation='relu', padding='same', input_shape=(48,48,1), data_format='channels_first'))
# model.add(Conv2D(64, kernel_size=(3, 3), activation='relu', padding='same', input_shape=(48,48,1)))
# model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))

# model.add(Conv2D(128, kernel_size=(3, 3), activation='relu', padding='same'))
# model.add(Conv2D(128, kernel_size=(3, 3), activation='relu', padding='same'))
# model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))

# model.add(Conv2D(256, kernel_size=(3, 3), activation='relu', padding='same'))
# model.add(Conv2D(256, kernel_size=(3, 3), activation='relu', padding='same'))
# model.add(Conv2D(256, kernel_size=(3, 3), activation='relu', padding='same'))
# model.add(Conv2D(256, kernel_size=(3, 3), activation='relu', padding='same'))
# model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))

# model.add(Conv2D(512, kernel_size=(3, 3), activation='relu', padding='same'))
# model.add(Conv2D(512, kernel_size=(3, 3), activation='relu', padding='same'))
# model.add(Conv2D(512, kernel_size=(3, 3), activation='relu', padding='same'))
# model.add(Conv2D(512, kernel_size=(3, 3), activation='relu', padding='same'))
# model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))

# model.add(Conv2D(512, kernel_size=(3, 3), activation='relu', padding='same'))
# model.add(Conv2D(512, kernel_size=(3, 3), activation='relu', padding='same'))
# model.add(Conv2D(512, kernel_size=(3, 3), activation='relu', padding='same'))
# model.add(Conv2D(512, kernel_size=(3, 3), activation='relu', padding='same'))
# model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
# model.add(Dropout(0.4))

# model.add(Flatten())
# model.add(Dense(4096, activation='relu'))
# model.add(Dense(4096, activation='relu'))
# model.add(Dense(7, activation='softmax'))
# def cnn_basic():
#     model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(48,48,1)))
#     model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
#     model.add(MaxPooling2D(pool_size=(2, 2)))
#     model.add(Dropout(0.5))

#     model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
#     model.add(MaxPooling2D(pool_size=(2, 2)))
#     model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
#     model.add(MaxPooling2D(pool_size=(2, 2)))
#     model.add(Dropout(0.5))

#     model.add(Flatten())
#     model.add(Dense(1024, activation='relu'))
#     model.add(Dropout(0.5))
#     model.add(Dense(7, activation='softmax'))

model = md.model_advanced()
# model.compile(loss='categorical_crossentropy',optimizer=Adam(lr=0.0001, decay=1e-6),metrics=['accuracy'])
model.compile(loss='mean_squared_error',optimizer=Adam(lr=0.0001, decay=1e-6),metrics=['accuracy'])

# Define data generators
train_dir = 'data/train'
val_dir = 'data/test'

num_train = 28709
num_val = 7178
batch_size = 128
num_epoch = 1000

train_datagen = ImageDataGenerator(rescale=1./255)
val_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
        train_dir,
        target_size=(48,48),
        batch_size=batch_size,
        color_mode="grayscale",
        class_mode='categorical')

validation_generator = val_datagen.flow_from_directory(
        val_dir,
        target_size=(48,48),
        batch_size=batch_size,
        color_mode="grayscale",
        class_mode='categorical')


early_stopping = EarlyStopping(monitor='val_accuracy', min_delta=0, patience=10, mode='max') #조기종료

model_info = model.fit(
    train_generator,
    validation_data=validation_generator,
    epochs=num_epoch,
    batch_size=batch_size,
    callbacks=[early_stopping]
)

    # validation_generator,
    # steps_per_epoch=num_train // batch_size,
    # validation_steps=num_val // batch_size,
# model_info = model.fit_generator(
#         train_generator,
#         steps_per_epoch=num_train // batch_size,
#         epochs=num_epoch,
#         validation_data=validation_generator,
#         validation_steps=num_val // batch_size)

nowtime = time.strftime('%Y%m%d_%H%M', time.localtime(time.time()))

plot_model_history(model_info)
model.save_weights(f'models/{nowtime}_model.h5')

with open(f'models/{nowtime}_log.txt', 'w') as f:
    f.write("batch_size: %s\n" %batch_size)
    f.write("num_epoch: %s \n\n" %num_epoch)

    with redirect_stdout(f):
        model.summary()
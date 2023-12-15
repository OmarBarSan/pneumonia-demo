import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dropout, Flatten, Dense

from utils.utils import preprocess_image

def modelo_ecualizado4():
    num_classes = 3
    model = Sequential()
    model.add(Conv2D(32, 3, padding='same', input_shape=(1024,1024,1), activation='relu'))
    model.add(Conv2D(32, 3, activation='relu'))
    model.add(Conv2D(32, 3, activation='relu'))
    model.add(MaxPooling2D((2,2)))
    model.add(Dropout(0.25))
    #model.add(Conv2D(32, 3, activation='relu'))

    # model.add(Conv2D(10, 3, padding='same', activation='relu'))
    # model.add(Conv2D(10, 3, activation='relu'))
    model.add(MaxPooling2D((2,2)))
    model.add(Dropout(0.25))
    model.add(MaxPooling2D((2,2)))
    model.add(Dropout(0.25))
    model.add(Flatten())
    # model.add(Dense(256, activation='relu'))
    # model.add(Dropout(0.25))
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.25))
    # model.add(Dense(64, activation='relu'))
    # model.add(Dropout(0.25))
    # model.add(Dense(32, activation='relu'))#borrar
    # model.add(Dropout(0.25))#borrar
    model.add(Dense(num_classes, activation='softmax'))


    print(model.summary())
    return model

def load_weights(model, path):
    model.load_weights(path)
    return model

def create_model(path):
    model = modelo_ecualizado4()
    model = load_weights(model, path)
    return model 

def make_prediction(model, frame):
    types = ["Normal", "Bacteria", "Virus"]
    frame = preprocess_image(frame)
    pred = model.predict(frame.reshape(-1,1024,1024,1), verbose=0)
    in_pred = np.argmax(pred)
    return types[in_pred]

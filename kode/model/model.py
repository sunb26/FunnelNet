import keras.layers as layers
from keras import Sequential

# ====================================================================================
# ====================================================================================
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! # of Parameter: 4145 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# ====================================================================================
# ====================================================================================

# def get_model(shape, num_classes):
#     model = Sequential()
#     model.add(layers.Conv2D(12, (2, 2), activation="tanh", input_shape=(shape)))
#     model.add(layers.MaxPooling2D((2, 2)))
#     model.add(layers.Conv2D(8, (2, 2)))
#     model.add(layers.MaxPooling2D((2, 2)))
#     model.add(layers.DepthwiseConv2D((2, 2), activation="tanh"))
#     model.add(layers.MaxPooling2D((2, 2)))
#     model.add(layers.Conv2D(8, (2, 2)))
#     model.add(layers.MaxPooling2D((2, 2)))
#     model.add(layers.Conv2D(12, (2, 2), activation="tanh", padding="same"))
#     model.add(layers.MaxPooling2D((2, 2), padding="same"))
#     model.add(layers.Flatten())
#     model.add(layers.Dropout(0.5))
#     model.add(layers.Dense(8, activation="relu"))

#     actv_fnc = "sigmoid" if num_classes == 1 else "softmax"
#     model.add(layers.Dense(num_classes, activation=actv_fnc))

#     return model

# ====================================================================================
# ====================================================================================
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! # of Parameter: 5453 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# ====================================================================================
# ====================================================================================

# def get_model(shape, num_classes):
#     model = Sequential()
#     model.add(layers.Conv2D(16, (2, 2), activation="tanh", input_shape=(shape)))
#     model.add(layers.MaxPooling2D((2, 2)))
#     model.add(layers.Conv2D(8, (2, 2)))
#     model.add(layers.MaxPooling2D((2, 2)))
#     model.add(layers.DepthwiseConv2D((2, 2), activation="tanh"))
#     model.add(layers.MaxPooling2D((2, 2)))
#     model.add(layers.Conv2D(8, (2, 2)))
#     model.add(layers.MaxPooling2D((2, 2)))
#     model.add(layers.Conv2D(16, (2, 2), activation="tanh", padding="same"))
#     model.add(layers.MaxPooling2D((2, 2), padding="same"))
#     model.add(layers.Flatten())
#     model.add(layers.Dropout(0.5))
#     model.add(layers.Dense(8, activation="relu"))

#     actv_fnc = "sigmoid" if num_classes == 1 else "softmax"
#     model.add(layers.Dense(num_classes, activation=actv_fnc))

#     return model
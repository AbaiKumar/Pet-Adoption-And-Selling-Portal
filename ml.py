import numpy as np
from PIL import *
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image


class MatchingAlgorithm:
    # Load the pre-trained MobileNetV2 model
    def __init__(self):
        self.model = MobileNetV2(weights='imagenet')

    # Function to predict breed and habits
    def predict_breed_and_habits(self, image_path):
        img = image.load_img(image_path, target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array = preprocess_input(img_array)
        img_array = np.expand_dims(img_array, axis=0)

        predictions = self.model.predict(img_array)
        decoded_predictions = decode_predictions(predictions)[0]

        # Extract the top prediction
        top_prediction = decoded_predictions[0]
        breed = top_prediction[1].replace("_", " ")

        return breed.title()

ml = MatchingAlgorithm()
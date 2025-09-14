import numpy as np
import tensorflow as tf

class TFLiteImageClassifier:
    def __init__(self, model_path, img_height, img_width):
        # Initialise with the model path and image size
        self.model_path = model_path
        self.img_height = img_height
        self.img_width = img_width
        self.interpreter = self.load_tflite_model()
        self.input_details, self.output_details = self.get_input_output_tensors()

    # Load and preprocess the image
    def load_and_preprocess_image(self, image_path):
        img = tf.keras.utils.load_img(image_path, target_size=(self.img_height, self.img_width))
        img_array = tf.keras.utils.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)  # Create a batch
        img_array = img_array.astype(np.float32)       # Ensure the input type is float32
        return img_array

    # Load the TensorFlow Lite model
    def load_tflite_model(self):
        interpreter = tf.lite.Interpreter(model_path=self.model_path)
        interpreter.allocate_tensors()
        return interpreter

    # Get input and output tensors
    def get_input_output_tensors(self):
        input_details = self.interpreter.get_input_details()
        output_details = self.interpreter.get_output_details()
        return input_details, output_details

    # Run inference
    def run_inference(self, input_data):
        input_index = self.input_details[0]['index']
        output_index = self.output_details[0]['index']
        
        self.interpreter.set_tensor(input_index, input_data)
        self.interpreter.invoke()
        
        output_data = self.interpreter.get_tensor(output_index)
        return output_data

    # Make predictions
    def predict(self, image_path):
        # Load and preprocess the image
        img_array = self.load_and_preprocess_image(image_path)

        # Run inference
        output_data = self.run_inference(img_array)

        # Process the output
        score = tf.nn.softmax(output_data[0])
        predicted_class = np.argmax(score)
        confidence = score[predicted_class].numpy() * 100

        return predicted_class, confidence
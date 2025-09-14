import sys
import os
import signal

# Add global packages
sys.path.append('/usr/lib/python3/dist-packages')
from picamera2 import Picamera2, Preview

# Add locally defined classes
from classes.TFLiteImageClassifier import TFLiteImageClassifier
from classes.EmailSender import EmailSender
from classes.LEDController import LEDController
# Dynamically add the submodule path to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), 'MFRC522-python'))
import MFRC522
import time
from dotenv import load_dotenv

# Initialise global flag
continue_reading = True
model_path = 'model2.tflite'
captured_image = 'image.jpg'
class_names = [
  'BackColour',
  'BackDL',
  'BackOther',
  'BackUC',
  'Blank',
  'FrontColour',
  'FrontDL',
  'FrontOther',
  'FrontUC'
]

load_dotenv()
EMAIL = os.getenv('EMAIL')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
PATH_TO_CAPTURED_IMAGE = os.getenv('PATH_TO_CAPTURED_IMAGE')


# Function to convert UID to string
def uid_to_string(uid):
    mystring = ""
    for i in uid:
        mystring = format(i, '02X') + mystring
    return mystring

# Signal handler for exiting the loop
def end_read(signal, frame):
    global continue_reading
    print("Ctrl+C captured, ending read.")
    continue_reading = False

def setup_camera_preview():
    cam = Picamera2()
    campreconfig = cam.create_preview_configuration(main={"size": (1000,1000)})
    cam.configure(campreconfig)
    cam.start_preview(Preview.QTGL)
    cam.start()
    return cam

def capture_and_save_image(cam):
    cam.capture_file(f"{PATH_TO_CAPTURED_IMAGE}/{captured_image}")

def delete_image():
    os.remove(f"{PATH_TO_CAPTURED_IMAGE}/{captured_image}")

def main():
  # Hook the SIGINT
  signal.signal(signal.SIGINT, end_read)

  # Create an object of the class MFRC522
  MIFAREReader = MFRC522.MFRC522()

  # Create an object of the class LEDController
  led_controller = LEDController(23, 16)

  # Setup the camera preview
  cam = setup_camera_preview()

  # Initialise the TensorFlow Lite Model
  classifier = TFLiteImageClassifier(model_path, img_height=500, img_width=500)
  email_sender = EmailSender(EMAIL, EMAIL_PASSWORD, EMAIL)

  # Welcome message
  print("Ready to scan for cards.\nPress Ctrl-C to stop.")

  # This loop keeps checking for chips.
  # If one is near it will get the UID and pass it to the TF Lite model
  while continue_reading:

      # Scan for cards
      (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

      # If a card is found
      if status == MIFAREReader.MI_OK:

          # Get the UID of the card
          (status, uid) = MIFAREReader.MFRC522_SelectTagSN()
          # If we have the UID, continue
          if status == MIFAREReader.MI_OK:
              print("-----------------------------------------------------")
              print("Card read UID: %s" % uid_to_string(uid))
              time.sleep(1)
              start = time.time()
              # Capture and save image
              capture_and_save_image(cam)
              
              if os.path.exists(f"/home/group6/clone-guard-part-b/{captured_image}"):
                
                # Predict the class of the captured image
                predicted_class, confidence = classifier.predict(captured_image)
                print(f"Predicted class: {class_names[predicted_class]}")
                print(f"Confidence score: {confidence:.2f}%")
                if (class_names[predicted_class] == 'FrontUC' or class_names[predicted_class] == 'BackUC') and confidence > 75:
                  end = time.time()
                  led_controller.turn_on_success_led()
                  print('Success!')
                else:
                  end = time.time()
                  led_controller.turn_on_failure_led()
                  print('Failure!')
                  email_sender.send_email(captured_image, uid_to_string(uid))
                print (f"Time taken: {end - start:.2f} seconds")

                # Delete captured image once prediction is made
                delete_image()
                print("-----------------------------------------------------")
          else:
              print("Failed to read UID")


if __name__ == "__main__":
  main()

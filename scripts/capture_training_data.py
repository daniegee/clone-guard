from picamera2 import Picamera2, Preview
import time

cam = Picamera2()
camconfig = cam.create_still_configuration(main={"size": (1000,1000)})
campreconfig = cam.create_preview_configuration(main={"size": (1000,1000)})
cam.configure(campreconfig)
cam.start_preview(Preview.QTGL)
cam.start()

cam.set_controls({"FrameRate": 30})

time.sleep(5)

path_to_folder = "PATH_TO_YOUR_STORE_IMAGES"
folder_name = "CLASS_NAME"
image_prefix = "CLASS_NAME"

for i in range(1, 51):
    image_path = f"{path_to_folder}/{folder_name}/{image_prefix}{i}.jpg"
    cam.capture_file(image_path)
    print(f"Captured image {i} of 100")
    time.sleep(0.25)

cam.stop()

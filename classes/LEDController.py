from gpiozero import LED
from time import sleep

class LEDController:
    def __init__(self, red_pin, green_pin):
        try:
            self.red_led = LED(red_pin)
            self.green_led = LED(green_pin)
            print("LEDs initialised successfully.")
        except Exception as e:
            print(f"Error initialising LEDs: {e}")
    
    def turn_on_success_led(self):
        try:
            self.green_led.on()
            sleep(2)
            self.green_led.off()
        except Exception as e:
            print(f"Error controlling GREEN LED: {e}")

    def turn_on_failure_led(self):
        try:
            self.red_led.on()
            sleep(2)
            self.red_led.off()
        except Exception as e:
            print(f"Error controlling RED LED: {e}")

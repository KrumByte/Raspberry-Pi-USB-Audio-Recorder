from gpiozero import Button, LED
import subprocess
import time
import os
from datetime import datetime

BUTTON_PIN = 17
LED_PIN = 27
OUTPUT_DIR = "/home/jackk/recordings"
os.makedirs(OUTPUT_DIR, exist_ok=True)

button = Button(BUTTON_PIN, pull_up=True)
led = LED(LED_PIN)

recording = False
process = None

def start_recording():
    global recording, process
    # The current date and time to create a unique filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # Create the output filename with the timestamp
    filename = f"{OUTPUT_DIR}/rec_{timestamp}.wav"
    print(f"Recording started: {filename}")
    # Start the arecord process to record audio from the microphone
    process = subprocess.Popen(["arecord", "-D", "hw:1,0", "-f", "cd", "-t", "wav", "-c", "1", filename])
    recording = True
    # Flash while recording
    led.blink(on_time=0.3, off_time=0.3)  

def stop_recording():
    global recording, process
    if process:
        process.terminate()
        process = None
    recording = False
    led.off()
    print("Recording stopped.")

def button_pressed():
    if not recording:
        start_recording()
    else:
        stop_recording()

button.when_pressed = button_pressed

print("Field recorder ready. Press button to start/stop.")
# Keep the script running to listen for button presses
try:
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    if recording:
        stop_recording()
    print("Shutting down.")
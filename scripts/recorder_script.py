from gpiozero import Button, LED, PWMLED
import subprocess
import time
import os
from datetime import datetime

BUTTON_PIN = 5
RLED_PIN = 25
GLED_PIN = 22
# Change the output directory to your desired path
OUTPUT_DIR = "/home/USER/recordings"

button = Button(BUTTON_PIN, pull_up=True)
rled = LED(RLED_PIN)
gled=LED(GLED_PIN)

recording = False
process = None

def get_mic_device():
    # Use arecord to list devices and find the one with "TC777" in its name
    result = subprocess.run(["arecord", "-l"], capture_output=True, text=True)
    for line in result.stdout.splitlines():
        if "TC777" in line:
            card_num = line.split("card ")[1].split(":")[0]
            return f"hw:{card_num},0"
    return "hw:0,0"  # fallback

def start_recording():
    global recording, process
    # Create the output directory if it doesn't exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    # Generate a timestamped filename for the recording
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{OUTPUT_DIR}/rec_{timestamp}.wav"
    print(f"Recording started: {filename}")
    device = get_mic_device()
    # Start the recording process using arecord
    process = subprocess.Popen(["arecord", "-D", device, "-f", "cd", "-t", "wav", "-c", "1", filename])
    recording = True
    #Blink the red LED to indicate recording status
    rled.blink(on_time=0.3, off_time=0.3)

def stop_recording():
    global recording, process
    if process:
        process.terminate()
        process = None
    recording = False
    rled.off()
    print("Recording stopped.")

def button_pressed():
    if not recording:
        start_recording()
    else:
        stop_recording()

gled.on()
button.when_pressed = button_pressed

print("Field recorder ready. Press button to start/stop.")
try:
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    if recording:
        stop_recording()
        gled.off()
    print("Shutting down.")

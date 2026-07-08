# Raspberry-Pi-USB-Audio-Recorder
## A Brief History:
As I started making some videos for myself around different local parks, I found over time that I would really be needing myself a portable microphone. I had a few USB microphones lying around, and thought, why not use that? Sadly I couldn't really find a good way to connect my USB Mic to my camera, so I looked to portable recorders. These things can go for pretty hefty price, and being someone who likes to save their money, the DIY thought was becoming pretty considerable. It would also serve as a great introduction into sauldering I thought. So I embarked on the journey to create my own portable microphone. 
## Features:
- When ready, green light turns on
- Button to start and stop recording
- Flashing Red Indicator light
- Saves files by Year/Month/Day - Hours/Minutes/Seconds
- Script continues running until power off of device.

## How To Make Your Own:
### Required Materials:
You don't need much for this project, all you need is:
- Raspberry Pi Zero 2 W
- USB A to Micro USB adapter
- A Power Supply ([I Used a USB A to Micro USB cable plugged into a portable battery](https://www.anker.com/products/a1229?variant=37438231806102))
- A [Red LED](https://www.adafruit.com/product/4203)
- A [Green LED](https://www.adafruit.com/product/4203)
- A [Push Button](https://www.adafruit.com/product/367)
- An HDMI to Micro HDMI adapter if you don't want to ssh.
- A Sauldering Station
- 1/2 Inch Wide Strips of Velcro.
- A USB Microphone
- 3, 250 ohm resistors (I would actually recommend something higher here, the LED's turn out very bright with this low of a resistance.)
- Insulated Wire
- Hot Glue
### Setting Up The Raspberry Pi Zero 2 W:
1. To start out, you need to install the an OS onto the Raspberry Pi, I went with the Raspberry Pi OS Lite, you can download it [here](https://www.raspberrypi.com/software/operating-systems/), or use their official Pi Imager program. You can find more about this step on the Raspberry Pi Documentation [here](https://www.raspberrypi.com/documentation/computers/getting-started.html#install). 
2. After you complete the initial setup and **have it connected to internet**, you can update your system with `sudo apt update`.
3. After updating the system, you are going to need to get the script onto the Raspberry Pi. This can be done in many ways, you can write the script on the Pi, or you can use `scp` to transfer the script from your computer onto the Pi. You can learn how to use `scp` [here](https://linuxize.com/post/how-to-use-scp-command-to-securely-transfer-files/) If you choose to use `scp` I recommend doing step 4 before you upload the scipt to your Pi.
4. Now that the script is on your device, there are a few things you need to change. 
    - On line 11, change your output directory to your desired directory (Or just change user to your username for the pi to use that path).
    - On line 24, you will see an `if "TC777" in line:` this is checking that your desired microphone is connected I was using a [Tonor TC777](https://www.amazon.com/Microphone-TONOR-Podcasting-Compatible-TC-777/dp/B07WLWN2ZT?th=1) at the time, hence the `TC777` bit. Change this to a part of your microphone's name to have that be the default Mic. If you don't know your Mic's name then with the pi connected to a display or ssh'd into the Pi with the mic connected you can run the command `arecord -l` to find it's name.
    - If you want to change the output file format you can edit line 39 from `wav` to `mp3` for example.
5. After that we need to run the script on startup. Again, there are many ways of doing this. I went with a systemd service, which you can see here:
```
[Unit]
Description=Field Recorder
After=network.target

[Service]
ExecStart=/usr/bin/python3 /path/to/recorder.py
Restart=on-failure
RestartSec=5
User=User

[Install]
WantedBy=multi-user.target
``` 
Take note, both the `User=` and the `ExecStart=/usr/bin/python3` need to be changed. 

6. After this we need to run the service on boot, that can be done with these commands:
```
sudo systemctl daemon-reload
sudo systemctl enable recorder
sudo systemctl start recorder
```
7. After that, the Pi should be all setup.
### 3D Printing The Case:
3D Printing the case should be fairly straight forward.
1. Print the Base Case on its largest face. (Used tree supports).
2. Print the lid on its side, with the small lip on the biggest face closest to the baseplate. (Used tree supports).
### Sauldering The Board:
I would recommend pulling up [this](https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fdnycf48t040dh.cloudfront.net%2Ffit-in%2F840x473%2FRaspberry-pi-zero-2W-pin-diagram.png&f=1&nofb=1&ipt=eec10732db6b0868bf681ea66264effb8fa6cfe3f7bb84473805db2d109e74be) diagram before you saulder everything together.
1. First, you will want to saulder a wire to pin 5 of the Pi, then saulder the wire to a 250 ohm resistor, then saulder this onto the button. On the other side of the button saulder a wire from it to a ground connection on the board. 
2. For the Red LED saulder a wire from pin 25 to a 250 ohm resistor, then from that resistor to the long end of the LED. Then, from the short end, saulder a wire from there to ground.
3. For the Green LED, you want to do the same thing, but instead, utilize pin 22 on the Pi. 
### Final Assembly:
1. Insert the Pi into the case, make sure to align the Pi to the different sticks on the case.
2. Slot the LED's into the 5mm holes
3. Insert the button into the square 6mm hole. 
4. Use hot glue to keep everything in place (I did not hot glue the board, in case I wanted to reuse it for the future).
5. Cram the wires into the case with the lid
6. Thread the 1/2 inch velcro through the tunnels on the lid and case.
7. Plug in the power and USB cables. 

And badabing badaboom, you have yourself a handheld USB audio recorder.

## Final Comments
Overall I am pretty happy with this project. I will say, my sauldering expierience was miserable. I had nothing to hold my cables and pieces down but tape. I made a mess, but I feel it was worth it in the end. 

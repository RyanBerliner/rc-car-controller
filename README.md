# rc-car-controller

Remote control crawlers (like the g made r1 I'm using in this project) sometimes offer 4 wheel steering. From what I could find, there is no way to toggle between standard 4 wheel steering, and crab walk steering. Basically... how do you create a toggle to reverse servo direction of just the rear steering? Thats what this does. It uses the switch on a standard traxxas controller to toggle between standard and crab walk.

[Watch video demo on youtube](https://youtu.be/_udrgzlhfoo) or [find more info on my website](https://ryanberliner.com/gmade-r1-crab-walk-mod-servo-reversing).

## What are the different programs?

### crabtoggle.py

**This is the main program** that you see running in the video. I've it set to start up on boot... so you just turn the car on and you can toggle between standard 4 wheel turning, and crab walking.

### listen.py

A test program that will (roughly) detect variations in a PWM signal

### passthrough.py

A test program that will listen to a PWM signal and control a servo. This basically is just a "passthrough" of the value... to an observer the behavior of the servo based on the remote control actions is the same as if there was no custom software running in the middle.

### run.py

A test program that allows you to enter duty cycle to test the limits of a servo.

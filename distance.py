#!/usr/bin/python3
# encoding:utf-8

# Libraries
import RPi.GPIO as GPIO
import time
import asyncio
import alsaaudio

# set mixer
devices = alsaaudio.cards()
idx = devices.index('Headphones')
mixers = alsaaudio.mixers(idx)
print(mixers)
m = alsaaudio.Mixer(mixers[int(0)], cardindex=idx)

# GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

# set GPIO Pins
GPIO_TRIGGER = 15
GPIO_ECHO = 14

# set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

loop = asyncio.get_event_loop()


async def volume_up():
    # do things here
    vol = m.getvolume()
    vol = int(vol[0])
    while vol < 80:
        vol += 1
        m.setvolume(vol)
        time.sleep(0.05)


async def volume_down():
    # do things here
    vol = m.getvolume()
    vol = int(vol[0])
    while vol > 0:
        vol -= 1
        m.setvolume(vol)
        time.sleep(0.05)


# async def check(distance):
#     current_time = time.time()
#     target_time = current_time + 60
#     while time.time() == target_time:
#         volume_down()


def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)

    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    StartTime = time.time()
    StopTime = time.time()

    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()

    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()

    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2

    return distance


if __name__ == '__main__':
    try:
        while True:
            dist = distance()
            print("Measured Distance = %.1f cm" % dist)
            time.sleep(1)
            if dist < 200:
                loop.run_until_complete(volume_up())
                # loop.run_until_complete(check())
            else:
                loop.run_until_complete(volume_down())
                pass
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()

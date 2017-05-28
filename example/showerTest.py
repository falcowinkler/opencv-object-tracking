#!/usr/bin/env python

from time import sleep, strftime, localtime
import os
import RPi.GPIO as GPIO

chan_list = [7,8,9,10,11,23,24,25]

GPIO.setmode(GPIO.BCM)
GPIO.setup(chan_list, GPIO.OUT)

GPIO.output(chan_list, 0)

while True:
	for i in range(0, 8):
		GPIO.output(chan_list[i], GPIO.HIGH)
		print "ITERATION: {} PIN: {} STATUS: HIGH".format(i, chan_list[i])
		sleep(0.1)
		GPIO.output(chan_list[i], GPIO.LOW)
		print "ITERATION: {} PIN: {} STATUS: LOW".format(i, chan_list[i])
		sleep(0.2)
	sleep(1.0)

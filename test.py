#!/usr/bin/python
# -*- coding:utf-8 -*-
import psutil
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)
from bs4 import BeautifulSoup
import requests
import logging
from waveshare_epd import epd2in13_V2
import time
from PIL import Image,ImageDraw,ImageFont
import traceback
import socket
def extract_ip():
    st = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:       
        st.connect(('10.255.255.255', 1))
        IP = st.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        st.close()
    return IP
def get_crypto_price(coin):
    url = "https://www.google.com/finance/quote/"+coin+"-EUR"
    HTML = requests.get(url)
    soup = BeautifulSoup(HTML.text, 'html.parser')
    price = soup.find("div", attrs={'class':'YMlKec fxKbKc'}).text
    return price

def check_price():
  last_price = -1
  while True:
    crypto = 'EOS'
    price = get_crypto_price(crypto)
    if price != last_price:
       return price
       last_price = price
    time.sleep(3)


# logging.basicConfig(level=logging.DEBUG)
try:
    #logging.info("epd2in13_V2 Demo")
    
    epd = epd2in13_V2.EPD()
    # logging.info("init and Clear")
    epd.init(epd.FULL_UPDATE)
    epd.Clear(0xFF)

    # Drawing on the image
    font20 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 20)
    font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
    # # partial update
    # logging.info("4.show time...")
    time_image = Image.new('1', (epd.height, epd.width), 255)
    time_draw = ImageDraw.Draw(time_image)
    
    epd.init(epd.FULL_UPDATE)
    epd.displayPartBaseImage(epd.getbuffer(time_image))
    
    epd.init(epd.PART_UPDATE)
    while (True):
        time_draw.rectangle((10, 10, 250, 122), fill = 255)
        time_draw.text((0, 10),"("+extract_ip()+")", font = font20, fill = 0)
        time_draw.text((150, 10),"EOS/€", font = font20, fill = 0)
        time_draw.text((150,30),str(check_price()), font = font20, fill = 0)
        time_draw.text((0, 30),"disk : "+str(round(psutil.disk_usage("/").free/1024.0/1024.0/1024.0,1))+"GB", font = font20, fill = 0)
        time_draw.text((0, 50),"ram: "+str(427.0-round(psutil.virtual_memory().used/1024.0/1024.0,1))+"MB", font = font20, fill = 0)
        time_draw.text((0, 70),"cpu: "+str(psutil.cpu_percent())+"%", font = font20, fill = 0)
        time_draw.text((0, 90), time.strftime('%H:%M:%S'), font = font24, fill = 0)
        epd.displayPartial(epd.getbuffer(time_image))
    # epd.Clear(0xFF)
    # logging.info("Clear...")
    epd.init(epd.FULL_UPDATE)
    epd.Clear(0xFF)
    
    # logging.info("Goto Sleep...")
    epd.sleep()

except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    # logging.info("ctrl + c:")
    epd.init(epd.FULL_UPDATE)
    epd.Clear(0xFF)
    epd2in13_V2.epdconfig.module_exit()
    exit()





#"YMlKec fxKbKc"
#https://www.google.com/finance/quote/EOS-EUR

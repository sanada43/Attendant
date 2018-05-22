# -*- coding: utf-8 -*-

import binascii
import nfc
import time
import json
import requests
import RPi.GPIO as GPIO
import json #
import datetime
import sys
sys.path.append('./Direct')
sys.path.append('./RPA')

from goout import goout
from gowork import gowork 
from leavework import leavework
from returnwork import returnwork

from goRPA import goRPA
from outRPA import outRPA 

def white_callback(channel):
    print(channel)
    if channel==23:
        print("black callback")
    if GPIO.input(24)==GPIO.HIGH:
        print('shutdown')

			
def black_callback(channel):
    print(channel)
    if channel==24:
        print("white callback")
    if GPIO.input(23)==GPIO.HIGH:
        print('shutdown')


class MyCardReader(object):
    # POST先
    #trigger_url = 'http://YOUR_TIMECARD_SYSTEM_URL/'
	
    path = open('/home/pi/Attendance/honsya.json' , 'r') #ここが(1)
    ids = json.load(path) #ここが(2)
    # カードのIDmとユーザーの対応表
    """
    ids = {
        '012e4573fc0c2d55' : { 'name': '400777' }
    }
    """
    # ブザーが接続されたGPIOピン
    buzzer_pin = 25
    buzzer = None
    green_pin = 14
    red_pin = 15
    error_pin = 18

    def __init__(self):
        pass
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.buzzer_pin, GPIO.OUT)
        self.buzzer = GPIO.PWM(self.buzzer_pin, 1000)
	GPIO.setup(self.green_pin, GPIO.OUT)
	GPIO.setup(self.red_pin, GPIO.OUT)
	GPIO.setup(self.error_pin, GPIO.OUT)
        GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(24, GPIO.RISING, callback=black_callback, bouncetime=200)
        GPIO.add_event_detect(23, GPIO.RISING, callback=white_callback, bouncetime=200)
        self.sTime = datetime.time(7,00,00,000)
        self.eTime = datetime.time(17,30,00,000)
        
        GPIO.output(self.error_pin, GPIO.HIGH)
        GPIO.output(self.green_pin, GPIO.HIGH)
        GPIO.output(self.red_pin, GPIO.HIGH)
        tone = 600
        self.buzzer.ChangeFrequency(tone)
        self.buzzer.start(5)
        time.sleep(0.1)
        self.buzzer.stop()
        GPIO.output(self.error_pin, GPIO.LOW)
        GPIO.output(self.green_pin, GPIO.LOW)
        GPIO.output(self.red_pin, GPIO.LOW)

    def on_connect(self, tag):
        print "touched"
        print tag
        # Type3のタグだけを受け付ける
        if isinstance(tag, nfc.tag.tt3.Type3Tag):
            self.idm = binascii.hexlify(tag.idm)
            self.post(self.idm)
        return True

    def post(self, id):
        print(id)
        if self.ids.has_key(id):
            user = self.ids[id]
            print user['name']
            nowTime = datetime.datetime.now()
            nowTime = nowTime.time()
            print '%s時%s分%s.%s秒n' % (nowTime.hour, nowTime.minute, nowTime.second, nowTime.microsecond)
            
            if GPIO.input(23)==GPIO.HIGH:
                res = leavework(user['LoginID'],user['PassWord'])
                print('leavework')
            elif GPIO.input(24)==GPIO.HIGH:
                res = returnwork(user['LoginID'],user['PassWord'])
                print('return')
            elif nowTime >= self.sTime and nowTime  <= self.eTime:
                if user['name']=='400777':
                    res = goRPA()
                else:
                    res = gowork(user['LoginID'],user['PassWord'])
                print('start')
            else:
                if user['name']=='400777':
                    res = outRPA()
                else:
                    res = goout(user['LoginID'],user['PassWord'])
                print('end')
            print(res)
			
            # 成功したらピー。失敗したらブーと鳴らす
            if res.status_code == 200:
                tone = 1000
                GPIO.output(self.green_pin, GPIO.HIGH)
            else:
                tone = 300
                GPIO.output(self.red_pin, GPIO.HIGH)               
        else:
            print '未知のタグです'
            GPIO.output(self.red_pin, GPIO.HIGH)
            tone = 300
			
        self.buzzer.ChangeFrequency(tone)
        self.buzzer.start(10)
        time.sleep(0.2)
        self.buzzer.stop()
	GPIO.output(self.green_pin, GPIO.LOW)
        GPIO.output(self.red_pin, GPIO.LOW)

    def read_id(self):
        clf = nfc.ContactlessFrontend('usb')
        try:
            clf.connect(rdwr={'on-connect': self.on_connect})
        finally:
            clf.close()

if __name__ == '__main__':
    try:
        cr = MyCardReader()
        while True:
            print "touch card:"
            cr.read_id()
            print "released"
    # ここらへんよくわかってない
    except KeyboardInterrupt:
        pass

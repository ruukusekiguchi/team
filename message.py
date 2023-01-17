from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

import requests
import json
# from googletrans import Translator

import RPi.GPIO as GPIO
import time

# 初期設定
GPIO.setmode(GPIO.BCM)

# GPIO 15 をデジタル入力に設定
GPIO.setup(15, GPIO.IN)

city_name = "Monteria" # 主要な都市名はいけるっぽい。
API_KEY = "1d6ea2750cd6e958153b8995b195109f" # xxxに自分のAPI Keyを入力。
api = "http://api.openweathermap.org/data/2.5/weather?units=metric&q={city}&APPID={key}"

app = Flask(__name__)
line_bot_api = LineBotApi(
    'x8RYq66HvPixS9uNyxh4nHouG4ERQ+CA5IdjmTHp5SnNovChko+/dKo1Kl7OfaP2YE5wm6fPaSjvBWxuD/wZq4pcqQ/9c4lxzHgz3JD37Hc15pG9//6WWwqVK0QgVsSDqtB1zT9ikiir9Ekxz9FSzQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('fccb2c35a8cd49f062acb01a578a2fe2')

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)
    return 'OK'

mode = 0
place = ''
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    lineRes = event.message.text
    botRes = event.message.text
    #変数宣言
    global mode
    global place
    count = 0
    #表示モード
    if mode != 1:
        if lineRes == '地点登録':
            botRes = '登録モードです'
            mode = 1
        if lineRes == '確認':
            botRes = '表示モードです'
        if lineRes == '地点確認':
            if place != '':
                botRes = place
            else:
                botRes = '登録されていません'

        if lineRes == '削除':
            if place != '':
                place = ''
                botRes = '登録解除しました'
            else:
                botRes = '登録されていません'
            
        if lineRes == '開始':
            if place != '':
                # weather = '予報：雨'
                # line_bot_api.reply_message(
                # event.reply_token,
                # TextSendMessage(text=weather))
                try:
                    print ("stay")
                    # Ctrl-C 待ち
                    while True:  
                        if GPIO.input(15) == 0:
                            if count <= 2000:
                                print (count)
                                count = count + 1
                            else:
                                botRes = '観測地点で雨が降っています'
                                break
                except:
                    print ("interrupted")

                finally:
                    GPIO.cleanup()
            else:
                botRes = '地点が登録されていません'

    #登録モード
    else:
        if lineRes == '解除':
            mode = 0
            botRes = '解除しました'
        elif lineRes == '確認':
            botRes = '登録モードです'
        else:
            mode = 0
            place = lineRes
            botRes = lineRes + '：登録しました'
        
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=botRes))

if __name__ == "__main__":
    app.run()
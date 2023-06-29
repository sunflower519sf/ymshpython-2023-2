from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
from apscheduler.schedulers.background import BackgroundScheduler

import os
import json
with  open('setting.json', 'r', encoding='utf-8') as jfile:
    jdata = json.load(jfile)

sched = BackgroundScheduler()
app = Flask(__name__)

line_bot_api = LineBotApi(jdata['TOKEN'])
handler = WebhookHandler(jdata['SECRET'])
yourID = jdata['YOURID']

@app.route("/", methods=['GET'])
def hello():
    line_bot_api.push_message(yourID, TextMessage(text='機器人啟動'))

    return "啟動"

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent)
def handle_message(event):

    if event.message.type == "text":
        

        if event.message.text == "ymsh":
            message = TextSendMessage("https://www.ymsh.hcc.edu.tw/home")
            line_bot_api.reply_message(event.reply_token, [message])
        if event.message.text.startswith("義民"):
            message = TextSendMessage("https://www.ymsh.hcc.edu.tw/ischool/publish_page/18/")
            line_bot_api.reply_message(event.reply_token, [message])
        if "成績" in event.message.text:
            message = TextSendMessage("https://da01.ymsh.hcc.edu.tw/online/")
            line_bot_api.reply_message(event.reply_token, [message])


if __name__ == "__main__":
    sched.start()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

# -*- coding: utf-8 -*-
#Todo SQL対応 /run/secretにpostgreの環境変数
# URL

from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, LocationMessage, TextSendMessage, ImageMessage,
)

import os
import errno
import tempfile
import json
from gourmet import Gourmet
# import psycopg2

app = Flask(__name__)

with open('config.json','r') as f:
    config = json.load(f)

handler = WebhookHandler(config["handler"])
line_bot_api = LineBotApi(config["access_token"])
keyid = config["keyid"]

#static_tmp_path = os.path.join('/', 'tmp', 'static', 'tmp')
#static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
# static_tmp_path = "/tmp"

# SQLデータ置き場をコンテナにマウントする.
# function for create tmp dir for download content
# def make_static_tmp_dir():
#     try:
#         os.makedirs(static_tmp_path)
#     except OSError as exc:
#         if exc.errno == errno.EEXIST and os.path.isdir(static_tmp_path):
#             pass
#         else:
#             raise

# 返答ルールなんだっけ?
# デコレータ?
@app.route("/", methods=['POST'])
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
        abort(400)

    return 'OK'

# textをそのまま返す
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))

# 店情報
# 不正データには「ごめんね、難しいことはわからないんだ...」
# 食べたいもの->位置情報聞く->送信->リスト表示
@handler.add(MessageEvent, message=LocationMessage)
def handle_address(event):
    lat = event.message.latitude
    lng = event.message.longitude
    query = Gourmet(keyid=keyid,lat=lat,lng=lng)
    query.search()
    text = ""
    for r in query.restaurants:
        text += r + "\n"
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="%s...とかどうかな??" % text))

# 食べ物画像から評価する? 牛丼, おにぎりの具材?
@handler.add(MessageEvent, message=ImageMessage)
def handle_content_message(event):
    if isinstance(event.message, ImageMessage):
        ext = 'jpg'
    else:
        return

    message_content = line_bot_api.get_message_content(event.message.id)
    with tempfile.NamedTemporaryFile(dir=static_tmp_path, prefix=ext + '-', delete=False) as tf:
        for chunk in message_content.iter_content():
            tf.write(chunk)
        tempfile_path = tf.name

    dist_path = tempfile_path + '.' + ext
    dist_name = os.path.basename(dist_path)
    os.rename(tempfile_path, dist_path)

    image = Image.open(dist_path)
    grayimage = ImageOps.grayscale(image)
    number = plate_to_number(grayimage)

    line_bot_api.reply_message(
        event.reply_token, [
            # TextSendMessage(text='Save content.'),
            TextSendMessage(text=number+u"だね、お兄ちゃん!"),
#            TextSendMessage(text=request.host_url + os.path.join('tmp', dist_name))
#            TextSendMessage(text=request.host_url + os.path.join('static', 'tmp', dist_name))
        ])

if __name__ == "__main__":
    # make_static_tmp_dir()
    app.run(host = '0.0.0.0', port = 8000, threaded = True, debug = False)

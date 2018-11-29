# -*- coding: utf-8 -*-

#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.

import os
import sys
import json
import requests
from argparse import ArgumentParser

from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)

from linebot.models import *

#For Giphy API
API_KEY = '[YOUR_API_KEY]'

app = Flask(__name__)
LINE_CHANNEL_SECRET='[YOUR_LINE_CHANNEL_SECRET]'
LINE_CHANNEL_ACCESS_TOKEN='[YOUR_LINE_CHANNEL_ACCESS_TOKEN]'
# get channel_secret and channel_access_token from your environment variable
channel_secret = LINE_CHANNEL_SECRET
channel_access_token = LINE_CHANNEL_ACCESS_TOKEN

if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

def GetGif(keyword):
    url='https://api.giphy.com/v1/gifs/random?api_key='+API_KEY+'&tag='+keyword+'&rating=G'
    data=json.loads(requests.get(url).text)
    url=data['data']['image_url']
    return url

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def message_text(event):
    text = event.message.text

    if text == '飲料':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='來杯蜂蜜檸檬吧')
        )
    elif text == '貼圖':
        line_bot_api.reply_message(
            event.reply_token,
            StickerMessage(
                package_id="1",
                sticker_id="2")
        )
    elif text=='圖片':
        line_bot_api.reply_message(
            event.reply_token,
            ImageSendMessage(
                original_content_url='https://ccsys.niu.edu.tw/exam/img/NIU_mark.png', 
                preview_image_url='https://ccsys.niu.edu.tw/exam/img/NIU_mark.png')
        )
    elif text=='狗派':
        keyword='husky'
        url=GetGif(keyword)
        line_bot_api.reply_message(
            event.reply_token,
            ImageSendMessage(
                original_content_url=url, 
                preview_image_url=url)
        )
    elif text=='貓派':
        keyword='cat'
        url=GetGif(keyword)
        line_bot_api.reply_message(
            event.reply_token,
            ImageSendMessage(
                original_content_url=url, 
                preview_image_url=url)
        )
    elif text=='影片':
        line_bot_api.reply_message(
            event.reply_token,
            VideoSendMessage(
                original_content_url='https://media3.giphy.com/media/3KXKQ41Y0Tqve/giphy.mp4', 
                preview_image_url='https://media3.giphy.com/media/3KXKQ41Y0Tqve/giphy.mp4')
        )
    elif text=="地標":
        line_bot_api.reply_message(
            event.reply_token,
            LocationSendMessage(
                title='國立宜蘭大學',
                address='宜蘭縣宜蘭市神農路一段一號',
                latitude=24.746456,
                longitude=121.7466373
            )
        )
    elif text == "樣板":    
        buttons_template = TemplateSendMessage(
            alt_text='目錄 template',
            template=ButtonsTemplate(
                title='Template-樣板介紹',
                text='Template分為四種，也就是以下四種：',
                thumbnail_image_url='https://ccsys.niu.edu.tw/exam/img/NIU_mark.png',
                actions=[
                    MessageTemplateAction(
                        label='Buttons Template',
                        text='buttons'
                    ),
                    MessageTemplateAction(
                        label='Confirm template',
                        text='Confirm'
                    ),
                    MessageTemplateAction(
                        label='Carousel template',
                        text='Carousel template'
                    ),
                    MessageTemplateAction(
                        label='Image Carousel',
                        text='Image Carousel'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template)
    elif text=="buttons":
        btn_template = TemplateSendMessage(
            alt_text='Button Template',
            template=ButtonsTemplate(
                title='按鈕範例標題',
                text='按鈕範例內文',
                thumbnail_image_url='https://ccsys.niu.edu.tw/exam/img/NIU_mark.png',
                actions=[
                    MessageTemplateAction(
                        label='按鈕1',
                        text='按鈕1 內文'
                    ),
                    URITemplateAction(
                        label='按鈕2 URL',
                        uri='https://www.youtube.com/watch?v=2Z2VyaecpGc'
                    ),
                    PostbackTemplateAction(
                        label='按鈕3 POSTBACK',
                        text='postback text',
                        data='postbacks'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token,btn_template)
    elif text=="Confirm":
        confirm_template = TemplateSendMessage(
            alt_text='目錄',
            template= ConfirmTemplate(
                text='僅有兩種按鈕用於選擇',
                actions=[
                    PostbackTemplateAction(
                        label='狗派',text='狗派',data='dog'
                    ),
                    MessageTemplateAction(
                        label='貓派',text='貓派'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token,confirm_template)
    elif text=="Carousel template":
        Carousel_template = TemplateSendMessage(
            alt_text='目錄',
            template= CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://ccsys.niu.edu.tw/exam/img/NIU_mark.png',
                        title='Column1',
                        text='Column1',
                        actions=[
                            PostbackTemplateAction(
                                label='postback1',
                                text='postback text1',
                                data='postbacks'
                            ),
                            MessageTemplateAction(
                                label='message1',
                                text='message text1'
                            ),
                            URITemplateAction(
                                label='uri1',
                                uri='https://www.youtube.com/watch?v=2Z2VyaecpGc'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://ccsys.niu.edu.tw/exam/img/NIU_mark.png',
                        title='Column2',
                        text='Column2',
                        actions=[
                            PostbackTemplateAction(
                                label='postback2',
                                text='postback text2',
                                data='postbacks'
                            ),
                            MessageTemplateAction(
                                label='message2',
                                text='message text2'
                            ),
                            URITemplateAction(
                                label='uri2',
                                uri='https://www.youtube.com/watch?v=2Z2VyaecpGc'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://ccsys.niu.edu.tw/exam/img/NIU_mark.png',
                        title='Column3',
                        text='Column3',
                        actions=[
                            PostbackTemplateAction(
                                label='postback3',
                                text='postback text3',
                                data='postbacks'
                            ),
                            MessageTemplateAction(
                                label='message3',
                                text='message text3'
                            ),
                            URITemplateAction(
                                label='uri3',
                                uri='https://www.youtube.com/watch?v=2Z2VyaecpGc'
                            )
                        ]
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token,Carousel_template)
    elif text=="Image Carousel":
        Image_Carousel = TemplateSendMessage(
            alt_text='Image Carousel template',
            template=ImageCarouselTemplate(
                columns=[
                    ImageCarouselColumn(
                    image_url='https://ccsys.niu.edu.tw/exam/img/NIU_mark.png',
                    action=PostbackTemplateAction(
                        label='postback1',
                        text='postback text1',
                        data='postbacks'
                        )
                    ),
                    ImageCarouselColumn(
                    image_url='https://ccsys.niu.edu.tw/exam/img/NIU_mark.png',
                    action=PostbackTemplateAction(
                        label='postback2',
                        text='postback text2',
                        data='postbacks'
                        )
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token,Image_Carousel) 
    
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=text)
        )

@handler.add(PostbackEvent)
def handle_postback(event):
    postdata = event.postdata.data
    if postdata =='postbacks':
        line_bot_api.reply_message(
            event.reply_token,TextSendMessage(text='postback:回覆')
        )

if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', default=8000, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()

    app.run(debug=options.debug, port=options.port)

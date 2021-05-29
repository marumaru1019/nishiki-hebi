import os
import json
import logging

import azure.functions as func
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

from component.kintone import *

import requests
import time

# 環境変数を取得
access_token = os.environ['ACCESS_TOKEN']
channel_secret = os.environ['CHANNEL_SECRET']

# インスタンスを定義
line_bot_api = LineBotApi(access_token)
handler = WebhookHandler(channel_secret)


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    logging.info(req.headers)

    if req.headers.get('x-line-signature'):
        signature = req.headers.get('x-line-signature')
    elif req.headers.get('X-Line-Signature'):
        signature = req.headers.get('X-Line-Signature')

    # リクエストボディを取得
    body = req.get_body().decode()
    logging.error(body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        logging.info('invalid signature error')
        func.HttpResponse(status_code=400)

    return func.HttpResponse('ok', status_code=200)


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # set kintone Token
    #WARNING: kintone token must set under handle_message
    kintone_endpoint = os.environ['KINTONE_URL']
    kintone_token = os.environ['KINTONE_TOKEN']
    content = event.message.text
    user_id = event.source.user_id
    profile = line_bot_api.get_profile(event.source.user_id)
    user_name = profile.display_name

    params = make_params(user_name, content, user_id, 1)
    logging.info(params)
    # input data into kintone database
    input_data(kintone_endpoint, kintone_token, params)
    logging.info(kintone_token)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=content))

import os
import json
import logging

import azure.functions as func
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

# 環境変数を取得
access_token = os.environ['ACCESS_TOKEN']
channel_secret = os.environ['CHANNEL_SECRET']

# インスタンスを定義
line_bot = LineBotApi(access_token)
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
    line_bot.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))

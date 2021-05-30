import os
import json
import logging

import azure.functions as func
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URIAction,
    PostbackAction, DatetimePickerAction,
    CameraAction, CameraRollAction, LocationAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage, FileMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent,
    MemberJoinedEvent, MemberLeftEvent,
    FlexSendMessage, BubbleContainer, ImageComponent, BoxComponent,
    TextComponent, IconComponent, ButtonComponent,
    SeparatorComponent, QuickReply, QuickReplyButton,
    ImageSendMessage)

from component.kintone import *
from component.azure_nlp import *
from component.news import *

import requests
import time

# 環境変数を取得
access_token = os.environ['ACCESS_TOKEN']
channel_secret = os.environ['CHANNEL_SECRET']

# インスタンスを定義
line_bot_api = LineBotApi(access_token)
handler = WebhookHandler(channel_secret)

imgs = [
    "https://www.tv-asahi.co.jp/doraemon/cast/img/nobita.jpg",
    "https://www.tv-asahi.co.jp/doraemon/cast/img/nobita.jpg",
    "https://www.tv-asahi.co.jp/doraemon/cast/img/shizuka.jpg"
]

titles = [
    "サンプル8",
    "サンプル9",
    "サンプル10"
]

urls = [
    "https://www.tv-asahi.co.jp/doraemon/cast/",
    "https://www.amazon.co.jp/%E3%83%95%E3%82%A3%E3%82%AE%E3%83%A5%E3%82%A2%E3%83%BC%E3%83%84ZERO-%E3%83%89%E3%83%A9%E3%81%88%E3%82%82%E3%82%93-STAND-%E7%B4%84250mm-%E5%A1%97%E8%A3%85%E6%B8%88%E3%81%BF%E5%AE%8C%E6%88%90%E5%93%81%E3%83%95%E3%82%A3%E3%82%AE%E3%83%A5%E3%82%A2/dp/B085CH14TB",
    "https://www.amazon.co.jp/-/en/Spirits-Doraemon-Selection-Approximately-Pre-painted/dp/B084HQ6CHX/ref=pd_lpo_21_img_1/358-5152328-6019449?_encoding=UTF8&pd_rd_i=B084HQ6CHX&pd_rd_r=f6f73248-59bd-4b10-a1b6-4becf4e1a427&pd_rd_w=9V4TA&pd_rd_wg=phLQN&pf_rd_p=dc0198fa-c371-4787-b1e2-96ed0e4d45e8&pf_rd_r=A1G0AFGRF5FBFF3ZF7FC&psc=1&refRID=A1G0AFGRF5FBFF3ZF7FC"
]


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

    ########## 質問をデータベースへの登録 ############
    # params = q_params(user_name, content, user_id, 1)
    # logging.info(params)
    # # input data into kintone database
    # q_input(kintone_endpoint, kintone_token, params)
    # logging.info(kintone_token)
    #############################################

    if content == "質問したい！":
        logging.info("質問を開始します")
        buttons_questions = ButtonsTemplate(
            title='ユニシスへの質問の受付', text='質問の該当するタイプを選んでください', actions=[
                # startというデータのpostbackeventを発行
                PostbackAction(label='学業の悩みについて', data='学業'),
                PostbackAction(label='内定について', data='内定'),
                PostbackAction(label='プライベートについて', data='プライベート'),
                PostbackAction(label='その他', data='その他'),
            ])

        template_message = TemplateSendMessage(
            alt_text='Buttons alt text', template=buttons_questions)
        logging.info(template_message)
        line_bot_api.reply_message(event.reply_token, template_message)

    elif content == "ニュース教えて！":
        logging.info("ニュースのクローリングを開始します。")
        ###########################################
        #       ニュースをクローリングする処理         #
        ###########################################
        with open('./news.json') as f:
            message = json.load(f)

        # ニュースを更新する処理
        logging.info("ニュースの更新を開始します")
        message = change_news(message, imgs, titles, urls)
        # make_news(message)
        logging.info("ニュースの更新に成功しました")
        ####################
        line_bot_api.reply_message(
            event.reply_token,
            # alt_textがないとエラーになるので注意
            FlexSendMessage(alt_text='ニュース', contents=message)
        )
    ################ 自然言語解析 ##################
    else:
        az = AzureNlp()
        logging.info("アジュールで読み込みを開始します")
        logging.info(os.listdir())
        message = az.response_message([content])

        if len(content) >= 2:
            logging.info("".join([content[-2], content[-1]]))

            if "".join([content[-2], content[-1]]) == "ゆに" or "".join([content[-2], content[-1]]) == "ユニ":
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text=message+"ゆにゆに"))
            else:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text=message))
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=message))
    #############################################

@handler.add(PostbackEvent)
def handle_postback(event):
    # set kintone Token
    #WARNING: kintone token must set under handle_message
    kintone_endpoint = os.environ['KINTONE_URL']
    kintone_token = os.environ['KINTONE_TOKEN']
    user_id = event.source.user_id
    profile = line_bot_api.get_profile(event.source.user_id)
    user_name = profile.display_name
    data = event.postback.data

    if data in ["学業", "内定", "プライベート", "その他"]:
        message = "質問内容を記入してください"
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=message))

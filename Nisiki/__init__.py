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

NEWS_URL = 'https://cu.unisys.co.jp'


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
    kintone_token2 = os.environ['KINTONE_TOKEN2']
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
        ###########################################
        #       ニュースをクローリングする処理         #
        logging.info("ニュースのクローリングを開始します。")
        titles, urls, imgs = news_scraiping(NEWS_URL)
        logging.info("ニュースのクローリングが終了しました")
        logging.info(f"titleのサンプル{titles[0:2]}")
        ###########################################

        # ニュースを更新する処理
        with open('./news.json') as f:
            message = json.load(f)
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

    # 自己紹介用のフォーマット
    elif "の名前は" in content:
        try:
            message = f'あなたの名前は{content.replace("私の名前は","").replace("だよ！","")}だね！\nこれからよろしくね！'
            logging.info("名前を登録中")
            params = selfintro_params(
                line_name=user_name, line_id=user_id, name=content.replace("私の名前は", "").replace("だよ！", ""), ID=user_id)
            q_input(kintone_endpoint, kintone_token2, params)

        except:
            message = "自己紹介のフォーマットが間違っているよ😭"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=message))

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
    kintone_token2 = os.environ['KINTONE_TOKEN2']
    user_id = event.source.user_id
    profile = line_bot_api.get_profile(event.source.user_id)
    user_name = profile.display_name
    data = event.postback.data

    if data in ["学業", "内定", "プライベート", "その他"]:
        message1 = "以下のフォーマットに従って質問をしてね♫"
        message2 = f"{data}：質問内容"
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=[message1, message2]))

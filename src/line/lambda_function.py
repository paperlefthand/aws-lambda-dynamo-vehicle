import json
import logging
import os
import sys

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent,
    TextMessage,
    TextSendMessage,
)

channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)

if channel_secret is None:
    logging.error("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    logging.error("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)


def lambda_handler(event, context):
    try:
        header = event["headers"]
        logging.info("Request header: ", header)
        signature = header["x-line-signature"]
        body = event["body"]
        logging.info("Request body: ", body)
    except KeyError:
        logging.error(sys.exc_info())
        sys.exit(1)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        return {
            "statusCode": 400,
            "body": json.dumps(
                {
                    "message": "InvalidSignatureError",
                }
            ),
        }

    # if event is MessageEvent and message is TextMessage, then echo text
    for e in events:
        if not isinstance(e, MessageEvent):
            continue
        if not isinstance(e.message, TextMessage):
            continue

        line_bot_api.reply_message(e.reply_token, TextSendMessage(text=e.message.text))

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "message": "ok",
            }
        ),
    }

import base64
import hashlib
import hmac
import json

import boto3

# import pygourmet  # noqa: F401
from aws_lambda_powertools import Logger, Tracer
from linebot.v3.messaging import (
    ApiClient,
    # AsyncApiClient,
    # AsyncMessagingApi,
    Configuration,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
)

# from linebot.v3.webhook import WebhookParser

logger = Logger()
tracer = Tracer()

ssm_client = boto3.client("ssm")
# parameter_names = [
#     "/linesdk/channel_access_token",
#     "/linesdk/channel_secret",
#     "/hotpepper/keyid",
# ]
# missing_params = []
# for param in parameter_names:
#     try:
#         response = ssm_client.get_parameter(Name=param, WithDecryption=True)
#         value = response["Parameter"]["Value"]
#         match param:
#             case "/linesdk/channel_access_token":
#                 # channel_access_token = value
#                 configuration = Configuration(access_token=value)
#                 api_client = ApiClient(configuration)
#                 line_bot_api = MessagingApi(api_client)
#             case "/linesdk/channel_secret":
#                 channel_secret = value
#                 # parser = WebhookParser(value)
#             case "/hotpepper/keyid":
#                 keyid = value
#     except ssm_client.exceptions.ParameterNotFound:
#         missing_params.append(param)

line_bot_api = None
channel_secret = None
keyid = None

try:
    # initialize line_bot_api
    response = ssm_client.get_parameter(
        Name="/linesdk/channel_access_token", WithDecryption=True
    )
    channel_access_token = response["Parameter"]["Value"]
    configuration = Configuration(access_token=channel_access_token)
    api_client = ApiClient(configuration)
    line_bot_api = MessagingApi(api_client)

    # setting configuration
    response = ssm_client.get_parameter(
        Name="/linesdk/channel_secret", WithDecryption=True
    )
    channel_secret = response["Parameter"]["Value"]
    response = ssm_client.get_parameter(Name="/hotpepper/keyid", WithDecryption=True)
    keyid = response["Parameter"]["Value"]

except ssm_client.exceptions.ParameterNotFound:
    logger.critical("configuration is invalid")


# Boto3のElastiCacheクライアントの初期化
# elasticache = boto3.client("elasticache")
# endpoint = os.environ.get("ELASTICACHE_ENDPOINT")


@logger.inject_lambda_context(log_event=True)
@tracer.capture_lambda_handler
def lambda_handler(event, context):
    if line_bot_api is None:
        return {"statusCode": 400, "body": "channel_access_token is  invalid"}
    if channel_secret is None:
        return {"statusCode": 400, "body": "channel_secret is invalid"}
    if keyid is None:
        return {"statusCode": 400, "body": "keyid is invalid"}

    signature = event.get("headers").get("x-line-signature")
    body_str = event.get("body")

    hash = hmac.new(
        channel_secret.encode("utf-8"), body_str.encode("utf-8"), hashlib.sha256
    ).digest()
    signature_gen = base64.b64encode(hash)

    if signature != signature_gen.decode("utf-8"):
        error_message = "Invalid signature"
        logger.error(error_message)
        return {"statusCode": 400, "body": error_message}

    body = json.loads(body_str)
    logger.debug(f"{body=}")
    events = body.get("events", [])
    for event in events:
        if event["type"] != "message":
            continue
        if event["message"]["type"] == "text":
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event["replyToken"],
                    messages=[TextMessage(text=event["message"]["text"])],  # type: ignore
                )
            )

    return {"statusCode": 200, "body": "OK"}

    #     # Memcachedへのデータの保存（簡易的にキー名として'sample_key'を使用しています）
    #     # この部分はPythonのmemcachedクライアントを使って適切に実装する必要があります。
    #     # サンプルとしてここではダミーのコードを示します。
    #     # elasticache.set('sample_key', body)

    #     return {
    #         "statusCode": 200,
    #         "body": json.dumps({"message": "Data saved successfully"}),
    #     }
    # except Exception as e:
    #     logger.exception(e)
    #     return {
    #         "statusCode": 500,
    #         "body": json.dumps({"message": "Internal server error"}),
    #     }

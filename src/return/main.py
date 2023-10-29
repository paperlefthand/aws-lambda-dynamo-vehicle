import json
import os

import boto3
from aws_lambda_powertools.logging.logger import Logger

TABLE_NAME = os.environ["TABLE_NAME"]


dynamodb = boto3.client("dynamodb")


logger = Logger()


@logger.inject_lambda_context(log_event=True)
def lambda_handler(event, context):
    try:
        # POSTされたリクエストボディを取得
        request_body = json.loads(event["body"])
    except KeyError as e:
        logger.error(e)
        return {"statusCode": 400, "body": json.dumps("event body is required.")}

    user_id = request_body.get("user_id")

    if not is_valid_user_id(user_id):
        return {"statusCode": 400, "body": json.dumps("user_id is not set or invalid.")}

    # DynamoDBへの追加項目設定
    options = {
        "TableName": TABLE_NAME,
        "Item": {"UserId": {"S": user_id}, "VehicleId": {"S": "001"}},
    }

    try:
        dynamodb.put_item(**options)
    except Exception as e:
        logger.error(e)
        return {
            "statusCode": 500,
            "body": json.dumps(f"failed to add user_id={user_id}"),
        }

    message = f"user_id={user_id} added successfully."
    return {
        "statusCode": 200,
        "body": json.dumps(message),
    }


def is_valid_user_id(user_id: str) -> bool:
    """ユーザIDのvalidation

    Args:
        user_id (str): ユーザID
    """

    is_valid = bool(user_id)
    return is_valid

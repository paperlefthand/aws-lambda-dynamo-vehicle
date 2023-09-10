import json
import boto3
import os

TABLE_NAME = os.environ["TABLE_NAME"]
AWS_REGION = os.environ["AWS_REGION"]

def lambda_handler(event, context):

    dynamodb_config = {"region_name": AWS_REGION}
    dynamodb = boto3.resource('dynamodb', **dynamodb_config)
    table = dynamodb.Table(TABLE_NAME)
    
    response = table.scan()
    items = response['Items']
    
    return {
        'statusCode': 200,
        'body': json.dumps(items)
    }
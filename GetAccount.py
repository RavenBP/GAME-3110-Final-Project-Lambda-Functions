import json
import boto3
from boto3.dynamodb.conditions import Key, Attr

def lambda_handler(event, context):
    
    http_method = event['httpMethod']
    
    if http_method == "GET":
        username = event['queryStringParameters']['username']
    elif http_method == "POST":
        body = json.loads(event['body'])
        
        username = body['username']
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('AccountTable')
    
    response = table.query(
        KeyConditionExpression=Key('Username').eq(username)
        )
    items = response['Items']
    
    if items: # User was found
        return {
            'statusCode': 200,
            'body': json.dumps(items)
        }
    else: # User was not found
        return {
            'statusCode': 200, 
            'body': json.dumps('User not found')
        }
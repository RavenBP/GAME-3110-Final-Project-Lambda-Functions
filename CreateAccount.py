import json
import boto3
from boto3.dynamodb.conditions import Key, Attr

def lambda_handler(event, context):
    
    http_method = event['httpMethod']
    
    if http_method == "GET":
        username = event['queryStringParameters']['username']
        password = event['queryStringParameters']['password']
    elif http_method == "POST":
        body = json.loads(event['body'])
        
        username = body['username']
        password = body['password']
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('AccountTable')
    
    response = table.put_item(
        Item={
            'Username': username,
            'Password': password,
            'numWins': '0',
            'exp': '0'
        })
    
    return {
        'statusCode': 200,
        'body': json.dumps('Account Created')
    }

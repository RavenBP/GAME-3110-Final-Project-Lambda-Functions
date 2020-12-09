import json
import boto3
from boto3.dynamodb.conditions import Key, Attr

username = ' '
password = ' '

def lambda_handler(event, context):
    
    http_method = event['httpMethod']
    
    if http_method== "GET":
        username = event['queryStringParameters']['username']
        password = event['queryStringParameters']['password']
    elif http_method == "POST":
        body = json.loads(event['body'])
        
        username = body['username']
        password = body['password']
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('AccountTable')
    
    response = table.query(
        KeyConditionExpression=Key('Username').eq(username)
        )
    items = response['Items']
    
    if items: #Item with that username has been found
        if items[0]['Password'] == password: # Password matches that found associated with account
            return {'statusCode': 200, 'body': json.dumps('LOGGED IN')}
        else: # Password does not match
            return {'statusCode': 200, 'body': json.dumps('INCORRECT PASSWORD')}
    else: # No account with that name was found
        return {'statusCode': 200,'body': json.dumps('ACCOUNT DOES NOT EXIST')}
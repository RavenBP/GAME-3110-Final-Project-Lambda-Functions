import json
import boto3
from boto3.dynamodb.conditions import Key, Attr

def lambda_handler(event, context):
    
    http_method = event['httpMethod']
    
    if http_method == "GET":
        username = event['queryStringParameters']['username']
        nWins = event['queryStringParameters']['nwins']
        xp = event['queryStringParameters']['xp']
    elif http_method == "POST":
        body = json.loads(event['body'])
        
        username = body['username']
        nWins = body['nwins']
        xp = body['xp']
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('AccountTable')
    
    table.update_item(
        Key={
            'Username': username
        },
        UpdateExpression='SET numWins = :val1, exp =:val2',
        ExpressionAttributeValues={
            ':val1': nWins,
            ':val2': xp
        }
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps('Values Updated')
    }
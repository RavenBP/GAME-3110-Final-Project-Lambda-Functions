import json
import boto3
from boto3.dynamodb.conditions import Key, Attr

attemptedUsername = 'User0' # Initially set to 'User0' as 'User0' is the debug account

def lambda_handler(event, context):
    
    http_method = event['httpMethod']
    
    if http_method == "GET":
        attemptedUsername = event['queryStringParameters']['attemptedUsername']
    elif http_method == "POST":
         body = json.loads(event['body'])
         
         attemptedUsername = body['attemptedUsername']
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('AccountTable')
    
    response = table.query(
        KeyConditionExpression=Key('Username').eq(attemptedUsername)
        )
    items = response['Items']
    
    if items: # Item with that username has been found in table
        return {
            'statusCode': 200,
            'body': json.dumps('USERNAME ALREADY IN USE')
        }
    else: # No items with that username were found in the table
        return {
            'statusCode': 200,
            'body': json.dumps('USERNAME AVAILABLE')
        }
import boto3
import json
from boto3.dynamodb.conditions import Key

def lambda_handler(event, context):
    # DynamoDB setup
    dynamo_client = boto3.client('dynamodb')
    table_name = 'Inventory'

    # Get the key from the path parameters
    if 'pathParameters' not in event or 'id' not in event['pathParameters']:
        return {
            'statusCode': 400,
            'body': json.dumps("Missing 'id' path parameter")
        }

    key_value = event['pathParameters']['id']
    try:
        table = boto3.resource('dynamodb').Table(table_name)

        response = table.query(
                KeyConditionExpression=Key('id').eq(key_value)
            )

        item = response["Items"]

        item = response.get('Items', [])

        if not item:
            return {
                'statusCode': 404,
                'body': json.dumps('Item not found')
            }

        return {
            'statusCode': 200,
            'body': json.dumps(item, default=str)  
        }
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps(str(e))
        }
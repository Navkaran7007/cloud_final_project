import boto3
import json
from boto3.dynamodb.conditions import Key

def lambda_handler(event, context):
    # Initialize DynamoDB client
    dynamo_client = boto3.client('dynamodb')
    table_name = 'Inventory'

    # Extract the '_id' from the path parameters
    if 'pathParameters' not in event or 'id' not in event['pathParameters']:
        return {
            'statusCode': 400,
            'body': json.dumps("Missing 'id' path parameter")
        }

    key_value = event['pathParameters']['id']

    try:
        table = boto3.resource('dynamodb').Table(table_name)
        result = table.query(
            KeyConditionExpression=Key('id').eq(key_value)
        )

        for item in result["Items"]:
            dynamo_client.delete_item(
                TableName=table_name,
                Key={
                    'id': {'S': key_value},
                    'location_id': {'N': str(item["location_id"])}
                }
            )

        return {
            'statusCode': 200,
            'body': json.dumps(f"Item with ID {key_value} deleted successfully.")
        }
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error deleting item: {str(e)}")
        }

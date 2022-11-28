import json
import traceback

import boto3 as boto3


def record_transaction(event, context):
    # initialize a new dynamodb client
    dynamodb_client = boto3.client("dynamodb")

    # extract the request body from the event object
    request_body = event["body"]
    print(request_body)

    # load the json in the request body into a python object
    transaction = json.loads(request_body)
    print(transaction)

    # format the data for insertion into dynamodb
    item = {
        "transactionId": {"S": transaction["transactionId"]},
        "item": {"S": transaction["item"]},
        "quantity": {"N": transaction["quantity"]},
        "price": {"N": transaction["price"]}
    }

    # insert the item into dynamodb
    try:
        dynamodb_client.put_item(
            TableName="Transactions", Item=item
        )
        success = True
    except Exception as error:
        print(traceback.format_exc())
        success = False

    # create a successful response
    response_body = {
        "success": success
    }
    response = {"statusCode": 200, "body": json.dumps(response_body)}

    # respond
    return response

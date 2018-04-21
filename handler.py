import json


def create_response(body, code):
    return {
        "statusCode": 200,
        "body": json.dumps(body)
    }

def upload_bite(event, context):
    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event["body"]
    }
    response = create_response(body, 200)
    return response

    # Use this code if you don't use the http event with the LAMBDA-PROXY
    # integration
    """
    return {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "event": event
    }
    """

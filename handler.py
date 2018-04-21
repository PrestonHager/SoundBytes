import json
import boto3
import datetime

# set all the default global variables to None
dynamo_db = None
dynamo_table = None
s3_connection = None
s3_bucket = None

def init_dynamodb():
    global dynamo_db, dynamo_table                                      # set the variables we use to global.
    dynamo_db = boto3.resource("dynamodb", region_name="us-west-2")     # set the dynamo_db and dynamo_table variables to their
    dynamo_table = dynamodb.Table("NearbyFriendsUsers")                 # correct resources.
    return True                                                         # return True from the process.

def init_s3():
    global s3_connection                    # set the variables we use to global.
    s3_connection = boto3.client('s3')      # set the s3_connection to a client connection to s3 using boto3.
    return True                             # return True from the process.

def upload_s3(file_stream, key):
    global s3_connection                                                    # set the client variable we use to the global version.
    s3_connection.upload_fileobj(file_stream, "sound-bytes-bites", key)     # upload a file obj/stream to the s3 bucket.
    return True                                                             # return True from the process.

def create_response(body, code):
    # this will create an html readable response with a code.
    return {
        "statusCode": code,
        "body": json.dumps(body)
    }

def upload_bite(event, context):
    # get the arguemnts
    # initialize the dynamo DB and S3 connections.
    init_dynamodb()
    init_s3()
    # put an item with the bite's metadata
    biteIdRatio = table.get_item(Key = {"BiteId": "-1"})["Item"]["BiteIdNumber"].as_integer_ratio()             # get the current byte number.
    biteId = biteIdRatio[0] / float(biteIdRatio[1])                                                             # parse it
    biteId = int(biteId + 1)                                                                                    # and add one.
    dynamo_table.update_item(Key = {"BiteId": "-1"}, AttributeUpdates = {"BiteIdNumber": {"Value": biteId}})    # and update the item storing the current bite number.
    biteItem = {"BiteId": str(biteId), "BiteAudio": str(biteAudioPointer), "TimeStamp": datetime.datetime.now().isoformat()}
    dynamo_table.put_item(Item = biteItem)                                                                      # put the item into dynamo DB.
    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event["body"]
    }
    response = create_response(body, 201)                                                                       # return the response with code 201 (created).
    return response

    # Use this code if you don't use the http event with the LAMBDA-PROXY
    # integration
    """
    return {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "event": event
    }
    """

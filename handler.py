import boto3
import datetime
import json
import wave
from cgi import parse_header, parse_multipart
from io import BytesIO, BufferedReader
from tinytag import ID3

# set all the default global variables to None
dynamo_db = None
dynamo_table = None
s3_connection = None
s3_bucket = None

def init_dynamodb():
    global dynamo_db, dynamo_table                                      # set the variables we use to global.
    dynamo_db = boto3.resource("dynamodb", region_name="us-west-2")     # set the dynamo_db and dynamo_table variables to their
    dynamo_table = dynamo_db.Table("sound-bytes-bites-metadata")                 # correct resources.
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
    # initialize the dynamo DB and S3 connections.
    init_dynamodb()
    init_s3()
    # get the arguemnts
    c_type, c_data = parse_header(event['headers']['Content-Type'])
    assert c_type == 'multipart/form-data'
    c_data["boundary"] = bytes(c_data["boundary"], 'utf-8')
    file_data = parse_multipart(BytesIO(event['body'].encode('utf-8')), c_data)["file"][0]      # this is the audio file as a byte array.
    audio_file_stream = BytesIO(file_data)
    # put an item with the bite's metadata
    biteIdRatio = dynamo_table.get_item(Key = {"BiteId": "-1"})["Item"]["BiteIdNumber"].as_integer_ratio()      # get the current byte number.
    biteId = biteIdRatio[0] / float(biteIdRatio[1])                                                             # parse it
    biteId = int(biteId + 1)                                                                                    # and add one.
    dynamo_table.update_item(Key = {"BiteId": "-1"}, AttributeUpdates = {"BiteIdNumber": {"Value": biteId}})    # and update the item storing the current bite number.
    # first check the length of the wave file, needs to be under or at 2 minutes. and more than or equal to 3 seconds.
    mp3_tags = ID3(BufferedReader(audio_file_stream), len(file_data))
    mp3_tags.load(tags=True, duration=True, image=False)
    if mp3_tags.duration < 3 or mp3_tags.duration > 120:
        audio_file_stream.seek(0)
        body = {
            "error": "Audio file too short or too long.",
            "duration": mp3_tags.duration,
            "length": len(file_data),
            "l2": len(audio_file_stream.read()),
            "tags": str(mp3_tags)
        }
        return create_response(body, 400)
    # save the audio file into S3.
    biteAudioPointer = upload_s3(audio_file_stream, "{biteId}-bite-audio".format(biteId=biteId))
    # create the bite metadata item and save it to DynamoDB.
    biteItem = {"BiteId": str(biteId), "BiteAudio": str(biteAudioPointer), "TimeStamp": datetime.datetime.now().isoformat()}
    dynamo_table.put_item(Item = biteItem)                                                                      # put the item into dynamo DB.
    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!"
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

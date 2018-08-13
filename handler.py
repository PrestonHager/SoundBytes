import base64
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
    # set the variables we use to global.
    global dynamo_db, dynamo_table
    # set the dynamo_db and dynamo_table variables to their
    dynamo_db = boto3.resource("dynamodb", region_name="us-west-2")
    # correct resources.
    dynamo_table = dynamo_db.Table("sound-bytes-bites-metadata")
    # return True from the process.
    return True

def init_s3():
    # set the variables we use to global.
    global s3_connection
    # set the s3_connection to a client connection to s3 using boto3.
    s3_connection = boto3.client('s3')
    # return True from the process.
    return True

def upload_s3(file_stream, key):
    # set the client variable we use to the global version.
    global s3_connection
    # upload a file obj/stream to the s3 bucket.
    try:
        s3_connection.upload_fileobj(file_stream, "sound-bytes-bites", key)
    except Exception as err:
        return err
    # return True from the process.
    return True

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
    try:
        assert c_type == 'multipart/form-data'
    except:
        body = {
            "error": "File was not sent as multipart/form-data.",
            "error_no": 0
        }
    c_data["boundary"] = bytes(c_data["boundary"], 'utf-8')
    # this is the audio file as a byte array.
    multiparts = parse_multipart(BytesIO(event['body'].encode('utf-8')), c_data)
    file_data_raw = b''.join(multiparts["file"]).decode('utf-8')
    try:
        file_data = base64.b64decode(file_data_raw)
    except:
        body = {
            "error": "Audio file was not sent with base64 encoding.",
            "error_no": 1
        }
        return create_response(body, 400)
    audio_file_stream = BytesIO(file_data)
    # first check the length of the wave file, needs to be under or at 2 minutes. and more than or equal to 3 seconds.
    mp3_tags = ID3(BufferedReader(audio_file_stream), len(file_data))
    mp3_tags.load(tags=False, duration=True, image=False)
    if mp3_tags.duration < 2 or mp3_tags.duration > 121:
        body = {
            "error": "Audio file too short or too long.",
            "error_no": 2,
            "duration": mp3_tags.duration
        }
        return create_response(body, 400)
    # put an item with the bite's metadata
    # get the current byte number.
    biteIdRatio = dynamo_table.get_item(Key = {"BiteId": "-1"})["Item"]["BiteIdNumber"].as_integer_ratio()
    # parse it
    biteId = biteIdRatio[0] / float(biteIdRatio[1])
    # and add one.
    biteId = int(biteId + 1)
    # and update the item storing the current bite number.
    dynamo_table.update_item(Key = {"BiteId": "-1"}, AttributeUpdates = {"BiteIdNumber": {"Value": biteId}})
    # save the audio file into S3.
    audio_file_stream.seek(0) # first reset the audio stream to the start.
    assert upload_s3(audio_file_stream, "{biteId}-bite-audio.mp3".format(biteId=biteId))
    # create the bite metadata item and save it to DynamoDB.
    biteItem = {"BiteId": str(biteId), "BiteAudio": "{biteId}-bite-audio.mp3".format(biteId=biteId), "TimeStamp": datetime.datetime.now().isoformat()}
    # put the item into dynamo DB.
    dynamo_table.put_item(Item = biteItem)
    body = {
        "message": "Successfully uploaded Sound Bite.",
        "biteId": biteId
    }
    # return the response with code 201 (created).
    response = create_response(body, 201)
    return response

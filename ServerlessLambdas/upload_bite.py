class UploadBite:
    def __init__(self):
        # global imports
        global base64, boto3, datetime, wave, parse_header, parse_multipart, BytesIO, BufferedReader, ID3
        import base64, boto3, datetime, wave
        from cgi import parse_header, parse_multipart
        from io import BytesIO, BufferedReader
        from tinytag import ID3
        # set up the databases
        import databases
        self.database = databases.Databases()

    def upload_bite(self, event, context):
        # first authorize the upload. (the client must supply a client id.)
        self.database.init_auth_db()
        token = event["headers"]["Authorization"]
        try:
            client_item = self.database.auth_table.get_item(Key = {"ClientId": token})["Item"]
        except:
            body = {
                "err": "Invalid Client ID token.",
                "cod": 6
            }
            return self.database.create_response(body, 400)
        current_time = int((datetime.datetime.now() - datetime.datetime(year=1970, month=1, day=1, hour=0, second=0)).total_seconds())
        if client_item["Expires"]+1800 <= current_time:
            self.database.auth_table.delete_item(Key = {"ClientId": token})
            all_ids = self.database.auth_table.get_item(Key = {"ClientId": "-1"})["Item"]["AllIds"]
            all_ids.pop(all_ids.index(token))
            self.database.auth_table.update_item(Key = {"ClientId": "-1"}, AttributeUpdates = {"AllIds": {"Value": all_ids}})
            body = {
                "err": "Client ID token has expired.",
                "cod": 8
            }
            return self.database.create_response(body, 400)
        if client_item["Expires"] <= current_time:
            body = {
                "err": "Client ID token has expired. Please refresh.",
                "cod": 7
            }
            return self.database.create_response(body, 400)
        # initialize the dynamo DB and S3 connections.
        self.database.init_dynamodb()
        self.database.init_s3()
        # get the arguemnts
        c_type, c_data = parse_header(event['headers']['Content-Type'])
        try:
            assert c_type == 'multipart/form-data'
        except:
            body = {
                "err": "File was not sent as multipart/form-data.",
                "cod": 0
            }
            return self.database.create_response(body, 400)
        c_data["boundary"] = bytes(c_data["boundary"], 'utf-8')
        # this is the audio file as a byte array.
        multiparts = parse_multipart(BytesIO(event['body'].encode('utf-8')), c_data)
        file_data_raw = b''.join(multiparts["file"]).decode('utf-8')
        try:
            file_data = base64.b64decode(file_data_raw)
        except:
            body = {
                "err": "Audio file was not sent with base64 encoding.",
                "cod": 1
            }
            return self.database.create_response(body, 400)
        audio_file_stream = BytesIO(file_data)
        # first check the length of the wave file, needs to be under or at 2 minutes. and more than or equal to 3 seconds.
        mp3_tags = ID3(BufferedReader(audio_file_stream), len(file_data))
        mp3_tags.load(tags=False, duration=True, image=False)
        if mp3_tags.duration < 2 or mp3_tags.duration > 121:
            body = {
                "err": "Audio file too short or too long.",
                "cod": 2,
                "dur": mp3_tags.duration
            }
            return self.database.create_response(body, 400)
        # put an item with the bite's metadata
        # get the current byte number.
        biteIdRatio = self.database.dynamo_table.get_item(Key = {"BiteId": "-1"})["Item"]["BiteIdNumber"].as_integer_ratio()
        # parse it
        biteId = biteIdRatio[0] / float(biteIdRatio[1])
        # and add one.
        biteId = int(biteId + 1)
        # and update the item storing the current bite number.
        self.database.dynamo_table.update_item(Key = {"BiteId": "-1"}, AttributeUpdates = {"BiteIdNumber": {"Value": biteId}})
        # save the audio file into S3.
        audio_file_stream.seek(0) # first reset the audio stream to the start.
        assert self.database.upload_s3(audio_file_stream, "{biteId}-bite-audio.mp3".format(biteId=biteId))
        # create the bite metadata item and save it to DynamoDB.
        biteItem = {"BiteId": str(biteId), "BiteAudio": "{biteId}-bite-audio.mp3".format(biteId=biteId), "TimeStamp": datetime.datetime.now().isoformat()}
        # put the item into dynamo DB.
        self.database.dynamo_table.put_item(Item = biteItem)
        body = {
            "cod": 100,
            "bid": biteId
        }
        # return the response with code 201 (created).
        response = self.database.create_response(body, 201)
        return response

def run(e, c):
    return UploadBite().upload_bite(e, c)

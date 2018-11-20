class App:
    def __init__(self):
        # set all the default class variables to None
        self.dynamo_db = None
        self.dynamo_table = None
        self.s3_connection = None
        self.s3_bucket = None

    def _import(self, function):
        if function == "upload":
            global base64, boto3, datetime, wave, parse_header, parse_multipart, BytesIO, BufferedReader, ID3
            import base64
            import boto3
            import datetime
            import wave
            from cgi import parse_header, parse_multipart
            from io import BytesIO, BufferedReader
            from tinytag import ID3
        elif function == "respond":
            global json
            import json
        elif function == "login":
            global datetime, random
            import datetime
            import random
        elif function == "auth":
            global base64, boto3, hashlib, json, os
            import base64
            import boto3
            import hashlib
            import json
            import os
        elif function == "create_account":
            global base64, boto3, hashlib, json, re, os, DEFAULT_INTRESTS
            import base64
            import boto3
            import hashlib
            import json
            import re
            import os
            from intrests import DEFAULT_INTRESTS
        elif function == "refresh_client":
            global boto3, datetime, json, random
            import boto3
            import datetime
            import json
            import random
        elif function == "get_bites":
            global boto3, json
            import boto3
            import json

    def _init_dynamodb(self):
        # set the dynamo_db and dynamo_table variables to their
        self.dynamo_db = boto3.resource("dynamodb", region_name="us-west-2")

    def init_dynamodb(self):
        self._init_dynamodb()
        # correct resources.
        self.dynamo_table = self.dynamo_db.Table("sound-bytes-bites-metadata")
        # return True from the process.
        return True

    def init_auth_db(self):
        self._init_dynamodb()
        # set to point at auth table.
        self.auth_table = self.dynamo_db.Table("sound-bytes-auth")
        # return True from the process
        return True

    def init_users(self):
        self._init_dynamodb()
        # set to the user dynamodb table.
        self.users = self.dynamo_db.Table("sound-bytes-users")
        # return True from the proccess
        return True

    def init_s3(self):
        # set the s3_connection to a client connection to s3 using boto3.
        self.s3_connection = boto3.client('s3')
        # return True from the process.
        return True

    def upload_s3(self, file_stream, key):
        # upload a file obj/stream to the s3 bucket.
        try:
            self.s3_connection.upload_fileobj(file_stream, "sound-bytes-bites", key)
        except Exception as err:
            return err
        # return True from the process.
        return True

    def create_response(self, body, code):
        self._import("respond")
        # this will create an html readable response with a code.
        return {
            "statusCode": code,
            "body": json.dumps(body)
        }

    def refresh_client(self, event, context):
        self._import("refresh_client")
        self.init_auth_db()
        token = event["headers"]["Authorization"]
        try:
            client_item = self.auth_table.get_item(Key = {"ClientId": token})["Item"]
        except:
            body = {
                "err": "Invalid Client ID token.",
                "cod": 6
            }
            return self.create_response(body, 400)
        current_time = int((datetime.datetime.now() - datetime.datetime(year=1970, month=1, day=1, hour=0, second=0)).total_seconds())
        self.auth_table.delete_item(Key = {"ClientId": token})
        all_ids = self.auth_table.get_item(Key = {"ClientId": "-1"})["Item"]["AllIds"]
        all_ids.pop(all_ids.index(token))
        self.auth_table.update_item(Key = {"ClientId": "-1"}, AttributeUpdates = {"AllIds": {"Value": all_ids}})
        if client_item["Expires"]+1800 <= current_time:
            body = {
                "err": "Client ID token has expired.",
                "cod": 8
            }
            return self.create_response(body, 400)
        # check to see if the refresh token matches the client id.
        if client_item["RefreshToken"] != event["body"]:
            body = {
                "err": "Refresh token does not match Client ID token.",
                "cod": 9
            }
            return self.create_response(body, 400)
        # otherwise a new client id token can be created, and the old deleted.
        refresh_token = "%032x" % random.randrange(16**32)
        access_token = self.generate_client_id(client_item["User"], refresh_token, current_time)
        body = {
            "id": access_token, # used to request resources or attach to uploaded resources.
            "rt": refresh_token, # the refresh token is used to get a new access token.
            "iat": current_time, # the issued at time is the current time.
            "exp": 3600, # the access token is valid for 1 hour.
            "cod": 100 # the code is a success.
        }
        response = self.create_response(body, 200)
        return response

    def get_bites(self, event, context):
        self._import("get_bites")
        # initialize the authorization database so we can authenticate the user.
        self.init_auth_db()
        # for now just a test post will be put up infinitely.
        # eventually this will have a user put there token in Authorization header
        # then an AI will match posts to them, these post ids will be stored somewhere.
        if "Authorization" not in event["headers"]:
            body = {
                "err": "No Authorization header found.",
                "cod": 13
            }
            return self.create_response(body, 403)
        token = event["headers"]["Authorization"].strip("Token ")
        try:
            client_item = self.auth_table.get_item(Key = {"ClientId": token})["Item"]
        except:
            body = {
                "err": "Invalid Client ID token.",
                "cod": 6
            }
            return self.create_response(body, 403)
        body = {
            "cod": 100,
            "all_posts": [{"t":"Title Goes Here","b":"This is a body paragraph, the maximum is 256 characters long."}]
        }
        return self.create_response(body, 200)

    def upload_bite(self, event, context):
        self._import("upload")
        # first authorize the upload. (the client must supply a client id.)
        self.init_auth_db()
        token = event["headers"]["Authorization"]
        try:
            client_item = self.auth_table.get_item(Key = {"ClientId": token})["Item"]
        except:
            body = {
                "err": "Invalid Client ID token.",
                "cod": 6
            }
            return self.create_response(body, 400)
        current_time = int((datetime.datetime.now() - datetime.datetime(year=1970, month=1, day=1, hour=0, second=0)).total_seconds())
        if client_item["Expires"]+1800 <= current_time:
            self.auth_table.delete_item(Key = {"ClientId": token})
            all_ids = self.auth_table.get_item(Key = {"ClientId": "-1"})["Item"]["AllIds"]
            all_ids.pop(all_ids.index(token))
            self.auth_table.update_item(Key = {"ClientId": "-1"}, AttributeUpdates = {"AllIds": {"Value": all_ids}})
            body = {
                "err": "Client ID token has expired.",
                "cod": 8
            }
            return self.create_response(body, 400)
        if client_item["Expires"] <= current_time:
            body = {
                "err": "Client ID token has expired. Please refresh.",
                "cod": 7
            }
            return self.create_response(body, 400)
        # initialize the dynamo DB and S3 connections.
        self.init_dynamodb()
        self.init_s3()
        # get the arguemnts
        c_type, c_data = parse_header(event['headers']['Content-Type'])
        try:
            assert c_type == 'multipart/form-data'
        except:
            body = {
                "err": "File was not sent as multipart/form-data.",
                "cod": 0
            }
            return self.create_response(body, 400)
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
            return self.create_response(body, 400)
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
            return self.create_response(body, 400)
        # put an item with the bite's metadata
        # get the current byte number.
        biteIdRatio = self.dynamo_table.get_item(Key = {"BiteId": "-1"})["Item"]["BiteIdNumber"].as_integer_ratio()
        # parse it
        biteId = biteIdRatio[0] / float(biteIdRatio[1])
        # and add one.
        biteId = int(biteId + 1)
        # and update the item storing the current bite number.
        self.dynamo_table.update_item(Key = {"BiteId": "-1"}, AttributeUpdates = {"BiteIdNumber": {"Value": biteId}})
        # save the audio file into S3.
        audio_file_stream.seek(0) # first reset the audio stream to the start.
        assert self.upload_s3(audio_file_stream, "{biteId}-bite-audio.mp3".format(biteId=biteId))
        # create the bite metadata item and save it to DynamoDB.
        biteItem = {"BiteId": str(biteId), "BiteAudio": "{biteId}-bite-audio.mp3".format(biteId=biteId), "TimeStamp": datetime.datetime.now().isoformat()}
        # put the item into dynamo DB.
        self.dynamo_table.put_item(Item = biteItem)
        body = {
            "cod": 100,
            "biteId": biteId
        }
        # return the response with code 201 (created).
        response = self.create_response(body, 201)
        return response

    def generate_client_id(self, user, refresh_token, current_time):
        all_ids = self.auth_table.get_item(Key = {"ClientId": "-1"})["Item"]["AllIds"]
        id = "%032x" % random.randrange(16**32)
        while id in all_ids:
            id = "%032x" % random.randrange(16**32)
        all_ids.append(id)
        self.auth_table.update_item(Key = {"ClientId": "-1"}, AttributeUpdates = {"AllIds": {"Value": all_ids}})
        client_item = {"ClientId": id, "RefreshToken": refresh_token, "IssueTime": current_time, "Expires": current_time+3600, "User": user}
        self.auth_table.put_item(Item = client_item)
        return id

    def login(self, event, context):
        self._import("auth")
        self.init_users()
        data = json.loads(event["body"])
        try:
            user = self.users.get_item(Key = {"Username": data["username"]})["Item"]
        except:
            body = {
                "err": "Username was not found, or not given.",
                "cod": 3
            }
            print("username not found. data was " +  data["username"])
            return self.create_response(body, 400)
        print(data["password"])
        password_hash = hashlib.blake2b(bytes(data["password"], "utf-8"), salt=bytes(os.getenv('SALT', "123456abcdef"), "utf-8")).digest()
        print(password_hash)
        if password_hash != base64.b64decode(user["Password"]):
            body = {
                "err": "Password does not match for user.",
                "cod": 4
            }
            return self.create_response(body, 401)
        if user["Verified"] == False:
            body = {
                "err": "Please verify your email.",
                "cod": 12
            }
            print("email not verified for " +  data["username"] + ". declining login.");
            return self.create_response(body, 400)
        self._import("login")
        self.init_auth_db()
        current_time = int((datetime.datetime.now() - datetime.datetime(year=1970, month=1, day=1, hour=0, second=0)).total_seconds())
        refresh_token = "%032x" % random.randrange(16**32)
        access_token = self.generate_client_id(user["Username"], refresh_token, current_time)
        body = {
            "id": access_token, # used to request resources or attach to uploaded resources.
            "rt": refresh_token, # the refresh token is used to get a new access token.
            "iat": current_time, # the issued at time is the current time.
            "exp": 3600, # the access token is valid for 1 hour.
            "cod": 100, # the code is a success.
        }
        response = self.create_response(body, 200)
        return response

    def verify_json(self, data, params):
        for param in params:
            if param not in data:
                return param
        return False

    def create_account(self, event, context):
        self._import("create_account")
        self.init_users()
        data = json.loads(event["body"])
        verify = self.verify_json(data, ["username", "password", "email"])
        if verify:
            body = {
                "err": "The '{param}' parameter was not found in the supplied JSON.".format(param=verify),
                "cod": 11
            }
            return self.create_response(body, 400)
        try:
            self.users.get_item(Key = {"Username": data["username"]})["Item"]
            body = {
                "err": "Username is already taken.",
                "cod": 5
            }
            return self.create_response(body, 400)
        except:
            # validate the email string.
            # NOTE: the is a very basic regex and is not the complete offical.
            if not re.match(r"[a-zA-Z0-9\.-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9]+", data["email"]):
                body = {
                    "err": "Invalid email address.",
                    "cod": 10
                }
                return self.create_response(body, 400)
            password_hash = hashlib.blake2b(bytes(data["password"], "utf-8"), salt=bytes(os.getenv('SALT', "123456abcdef"), "utf-8")).digest()
            user = {"Username": data["username"], "Password": base64.b64encode(password_hash).decode("utf-8"), "Email": data["email"], "Verified": False, "Intrests": DEFAULT_INTRESTS}
            self.users.put_item(Item = user)
            body = {
                "cod": 101
            }
            return self.create_response(body, 201)

    def verify_email(self, event, context):
        body = {
            "cod": 100
        }
        return self.create_response(body, 200)

_inst = App()
upload_bite = _inst.upload_bite
login = _inst.login
create_account = _inst.create_account
refresh_client = _inst.refresh_client
verify_email = _inst.verify_email
get_bites = _inst.get_bites

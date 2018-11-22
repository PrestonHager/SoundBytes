class Databases:
    def __init__(self):
        # import anything that might be needed.
        global boto3, json
        import boto3, json
        # set all the default class variables to None
        self.dynamo_db = None
        self.dynamo_table = None
        self.auth_table = None
        self.users = None
        self.s3_connection = None
        self.s3_bucket = None

    def _init_dynamodb(self):
        # set the dynamo_db and dynamo_table variables to their
        self.dynamo_db = boto3.resource("dynamodb", region_name="us-west-2")
        # return True from the process
        return True

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
        # this will create an html readable response with a code.
        return {
            "statusCode": code,
            "body": json.dumps(body)
        }

    def generate_client_id(self, user, refresh_token, current_time):
        all_ids = self.database.auth_table.get_item(Key = {"ClientId": "-1"})["Item"]["AllIds"]
        id = "%032x" % random.randrange(16**32)
        while id in all_ids:
            id = "%032x" % random.randrange(16**32)
        all_ids.append(id)
        self.database.auth_table.update_item(Key = {"ClientId": "-1"}, AttributeUpdates = {"AllIds": {"Value": all_ids}})
        client_item = {"ClientId": id, "RefreshToken": refresh_token, "IssueTime": current_time, "Expires": current_time+3600, "User": user}
        self.database.auth_table.put_item(Item = client_item)
        return id

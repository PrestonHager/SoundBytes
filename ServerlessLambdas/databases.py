class Databases:
    def __init__(self):
        # import anything that might be needed.
        global boto3, json
        import boto3, json
        # set all the default class variables to None
        self.dynamo_db = None
        self.bites = None
        self.auth_table = None
        self.users = None
        self.verify_table = None
        self.s3_connection = None
        self.s3_bucket = None
        self.sts_client = None

    def init_sts(self):
        self.sts_client = boto3.client('sts')
        return True

    def _init_dynamodb(self):
        # set the dynamo_db and dynamo_table variables to their
        self.dynamo_db = boto3.resource("dynamodb", region_name="us-west-2")
        # return True from the process
        return True

    def init_bites_db(self):
        self._init_dynamodb()
        # correct resources.
        self.bites = self.dynamo_db.Table("soundbytes-bites-metadata")
        # return True from the process.
        return True

    def init_auth_db(self):
        self._init_dynamodb()
        # set to point at auth table.
        self.auth_table = self.dynamo_db.Table("soundbytes-auth")
        # return True from the process
        return True

    def init_users(self):
        self._init_dynamodb()
        # set to the user dynamodb table.
        self.users = self.dynamo_db.Table("soundbytes-users")
        # return True from the proccess
        return True

    def init_verify_table(self):
        self._init_dynamodb()
        # set to the verify dynamodb table.
        self.verify_table = self.dynamo_db.Table("soundbytes-verify")
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
            self.s3_connection.upload_fileobj(file_stream, "soundbytes-bites", key)
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

    def create_verify_link(self, username):
        import random
        all_links = self.verify_table.get_item(Key = {"LinkId": "-1"})["Item"]["AllLinks"]
        verify_link = "%016x" % random.randrange(16**16)
        while verify_link in all_links:
            verify_link = "%016x" % random.randrange(16**16)
        all_links.append(verify_link)
        self.verify_table.update_item(Key = {"LinkId": "-1"}, AttributeUpdates = {"AllLinks": {"Value": all_links}})
        self.verify_table.put_item(Item = {"LinkId": verify_link, "User": username})
        return "https://api.soundbytes.xyz/dev/verify?usr=" + verify_link

    def create_unsubscribe_link(self, email):
        from urllib import quote_plus
        return "https://api.soundbytes.xyz/dev/unsubscribe?email=" + quote_plus(email)

    def generate_client_id(self, user, refresh_token, current_time):
        import random
        # all_ids = self.auth_table.get_item(Key = {"ClientId": "-1"})["Item"]["AllIds"]
        id = "%032x" % random.randrange(16**32)
        # while id in all_ids:
        #     id = "%032x" % random.randrange(16**32)
        # all_ids.append(id)
        # self.auth_table.update_item(Key = {"ClientId": "-1"}, AttributeUpdates = {"AllIds": {"Value": all_ids}})
        auth_token = None
        client_item = {"ClientId": id, "RefreshToken": refresh_token, "IssueTime": current_time, "Expires": current_time+3600, "User": user}
        self.auth_table.put_item(Item = client_item)
        return id

    def get_credentials(self, session_name, resource_name=None):
        if resource_name == None:
            session_policy = {}
        else:
            session_policy = {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Action": "s3:PutObject",
                        "Resource": resource_name
                    }
                ]
            }
        response = self.client.assume_role(
            RoleArn="arn:aws:iam::105554980019:role/soundbytes-s3",
            RoleSessionName=session_name,
            Policy=json.dumps(session_policy)
        )
        credentials = response["Credentials"]
        if credentials != None:
            credentials["Expiration"] = credentials["Expiration"].isoformat()
            return credentials
        else:
            return False

    def send_email(self, to_address):
        pass

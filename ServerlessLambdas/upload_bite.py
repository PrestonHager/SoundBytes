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
        authorizer = event["requestContext"]["authorizer"]
        user_id = authorizer["principalId"]
        # initialize the dynamo DB and STS connections.
        self.database.init_bites_db()
        self.database.init_sts()
        # create a bite item pointing to a bite id path in s3
        biteId = 0
        biteItem = {"BiteId": str(biteId), "BiteAudio": "{biteId}-bite-audio.mp3".format(biteId=biteId)}
        # put the item into dynamo DB.
        self.database.bites.put_item(Item = biteItem)
        # give the user credentials to upload an audio file with STS
        uploadPath = "https://api.soundbytes.xyz/dev/upload"
        credentials = self.get_credentials(user_id, f"arn:aws:s3:::soundbytes-bites/{biteId}-audio.m4a")
        body = {
            "ByteId": biteId,
            "UploadTo": uploadPath,
            "Credentials": credentials
        }
        response = self.database.create_response(body, 201)
        return response


def run(e, c):
    return UploadBite().upload_bite(e, c)

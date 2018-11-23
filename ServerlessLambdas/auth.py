class Auth:
    def __init__(self):
        # global imports
        global base64, datetime, hashlib, json, os, random
        import base64, datetime, hashlib, json, os, random
        # set up the databases
        import databases
        self.database = databases.Databases()

    """
    Authorization Method: Used by AWS Lambda
    Parameters: event, context
    Output: html response
    """
    def auth(self, event, context):
        self.database.init_users()
        data = json.loads(event["body"])
        try:
            user = self.database.users.get_item(Key = {"Username": data["username"]})["Item"]
        except:
            body = {
                "err": "Username was not found, or not given.",
                "cod": 3
            }
            print("username not found. data was " +  data["username"])
            return self.database.create_response(body, 400)
        print(data["password"])
        password_hash = base64.b64encode(hashlib.blake2b(bytes(data["password"], "utf-8"), salt=bytes(os.getenv('SALT', "123456abcdef"), "utf-8")).digest()).decode("utf-8")
        print(password_hash)
        if password_hash != user["Password"]:
            body = {
                "err": "Password does not match for user.",
                "cod": 4
            }
            return self.database.create_response(body, 401)
        if user["Verified"] == False:
            body = {
                "err": "Please verify your email.",
                "cod": 12
            }
            print("email not verified for " +  data["username"] + ". declining login.");
            return self.database.create_response(body, 400)
        # Generate a token
        self.database.init_auth_db()
        current_time = int((datetime.datetime.now() - datetime.datetime(year=1970, month=1, day=1, hour=0, second=0)).total_seconds())
        refresh_token = "%032x" % random.randrange(16**32)
        access_token = self.database.generate_client_id(user["Username"], refresh_token, current_time)
        body = {
            "id": access_token, # used to request resources or attach to uploaded resources.
            "rt": refresh_token, # the refresh token is used to get a new access token.
            "iat": current_time, # the issued at time is the current time.
            "exp": current_time + 3600, # the access token is valid for 1 hour.
            "cod": 100, # the code is a success.
        }
        response = self.database.create_response(body, 201)
        return response

def run(e, c):
    return Auth().auth(e, c)

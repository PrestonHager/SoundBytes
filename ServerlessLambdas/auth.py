class Auth:
    def __init__(self):
        # global imports
        global base64, Branca, datetime, hashlib, json, os, random, secrets
        import base64, datetime, hashlib, json, os, random, secrets
        from branca import Branca
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
        try:
            data = json.loads(event["body"])
        except:
            body = {
                "err": "The post body must be in JSON format.",
                "cod": 21
            }
            return self.database.create_response(body, 400)
        try:
            user = self.database.users.get_item(Key = {"Username": data["username"].lower()})["Item"]
        except:
            body = {
                "err": "Username was not found, or not given.",
                "cod": 3
            }
            return self.database.create_response(body, 400)
        if "password" not in data:
            body = {
                "err": "Password was not given.",
                "cod": 4
            }
            return self.database.create_response(body, 400)
        password_hash = base64.b64encode(hashlib.blake2b(bytes(data["password"], "utf-8"), salt=bytes(os.getenv('SALT', "123456abcdef"), "utf-8")).digest()).decode("utf-8")
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
            print("email not verified for " +  data["username"].lower() + ". declining login.");
            return self.database.create_response(body, 400)
        # Generate a token
        auth_token = secrets.token_hex(64)
        branca_token = Branca(os.getenv('BRANCA_KEY', "d8b647974af437bdf761099cec8d3e5ac263037d02c8ad8498efc7eef27e0a33"))
        token = branca_token.encode(f"{user['Username']}:{auth_token}")
        user["AuthToken"] = auth_token
        body = {
            "auth_token": token,
        }
        response = self.database.create_response(body, 201)
        return response

def run(e, c):
    return Auth().auth(e, c)

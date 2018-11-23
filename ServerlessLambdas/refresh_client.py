class RefreshClient:
    def __init__(self):
        # global imports
        global datetime, random
        import datetime, random
        # set up the databases
        import databases
        self.database = databases.Databases()

    """
    Refresh Client Method: Used by AWS Lambda
    Parameters: event, context
    Output: html response
    """
    def refresh_client(self, event, context):
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
        self.database.auth_table.delete_item(Key = {"ClientId": token})
        all_ids = self.database.auth_table.get_item(Key = {"ClientId": "-1"})["Item"]["AllIds"]
        all_ids.pop(all_ids.index(token))
        self.database.auth_table.update_item(Key = {"ClientId": "-1"}, AttributeUpdates = {"AllIds": {"Value": all_ids}})
        if client_item["Expires"]+1800 <= current_time:
            body = {
                "err": "Client ID token has expired.",
                "cod": 8
            }
            return self.database.create_response(body, 400)
        # check to see if the refresh token matches the client id.
        if client_item["RefreshToken"] != event["body"]:
            body = {
                "err": "Refresh token does not match Client ID token.",
                "cod": 9
            }
            return self.database.create_response(body, 400)
        # otherwise a new client id token can be created, and the old deleted.
        refresh_token = "%032x" % random.randrange(16**32)
        access_token = self.database.generate_client_id(client_item["User"], refresh_token, current_time)
        body = {
            "id": access_token, # used to request resources or attach to uploaded resources.
            "rt": refresh_token, # the refresh token is used to get a new access token.
            "iat": current_time, # the issued at time is the current time.
            "exp": 3600, # the access token is valid for 1 hour.
            "cod": 100 # the code is a success.
        }
        response = self.database.create_response(body, 200)
        return response

def run(e, c):
    return RefreshClient().refresh_client(e, c)

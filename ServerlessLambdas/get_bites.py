class GetBites:
    def __init__(self):
        global datetime
        # set up the databases
        import databases
        import datetime
        self.database = databases.Databases()

    """
    Get Bites Method: Used by AWS Lambda
    Parameters: event, context
    Output: html response
    """
    def get_bites(self, event, context):
        # initialize the authorization database so we can authenticate the user.
        self.database.init_auth_db()
        # for now just a test post will be put up infinitely.
        # eventually this will have a user put in a query parameter with their token.
        # then an AI will match posts to them, these post ids will be stored somewhere.
        try:
            token = event["queryStringParameters"]["tkn"]
        except:
            body = {
                "err": "No token found in request.",
                "cod": 13
            }
            return self.database.create_response(body, 400)
        try:
            client_item = self.database.auth_table.get_item(Key = {"ClientId": token})["Item"]
        except:
            body = {
                "err": "Invalid Client ID token.",
                "cod": 6
            }
            return self.database.create_response(body, 403)
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
        body = {
            "cod": 100,
            "all_posts": [{"t":"Title Goes Here","b":"This is a body paragraph, the maximum is 256 characters long."}]
        }
        return self.database.create_response(body, 200)

def run(e, c):
    return GetBites().get_bites(e, c)

class GetBites:
    def __init__(self):
        # set up the databases
        import databases
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
        # eventually this will have a user put there token in Authorization header
        # then an AI will match posts to them, these post ids will be stored somewhere.
        if "Authorization" not in event["headers"]:
            body = {
                "err": "No Authorization header found.",
                "cod": 13
            }
            return self.database.create_response(body, 403)
        token = event["headers"]["Authorization"].strip("Token ")
        try:
            client_item = self.database.auth_table.get_item(Key = {"ClientId": token})["Item"]
        except:
            body = {
                "err": "Invalid Client ID token.",
                "cod": 6
            }
            return self.database.create_response(body, 403)
        body = {
            "cod": 100,
            "all_posts": [{"t":"Title Goes Here","b":"This is a body paragraph, the maximum is 256 characters long."}]
        }
        return self.database.create_response(body, 200)

def run(e, c):
    return CreateAccount().create_account(e, c)

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
        # for now just a test post will be put up infinitely.
        # eventually this will have a user put in a query parameter with their token.
        # then an AI will match posts to them, these post ids will be stored somewhere.
        # NOTE: first we will serve content based on followed users
        #       then we can make an algorithm to serve content
        authorizer = event["requestContext"]["authorizer"]
        user_id = authorizer["principalId"]
        body = {
            "cod": 100,
            "all_posts": [{"t":"Title Goes Here","b":"This is a body paragraph, the maximum is 256 characters long."}]
        }
        return self.database.create_response(body, 200)

def run(e, c):
    return GetBites().get_bites(e, c)

from responses import *

class VerifyEmail:
    def __init__(self):
        # set up the databases
        import databases
        self.database = databases.Databases()

    def verify_email(self, event, context):
        # initialize the verify table
        # find the usr param and get its value.
        self.database.init_verify_table()
        self.database.init_users()
        try:
            link_id = event["pathParameters"]["link_id"]
            username = self.database.verify_table.get_item(Key = {"LinkId": link_id})["Item"]["User"]
            # TODO: verify that the token was created by the server by checking the username inside the token (using the server key of course)
        except:
            return RESPONSE_FAILURE
        # if everything is a success then set Verified to True in user table.
        self.database.users.update_item(Key = {"Username": username}, AttributeUpdates = {"Verified": {"Value": True}})
        # remove the link_id from the verify table
        self.database.verify_table.delete_item(Key = {"LinkId": link_id})
        return RESPONSE_SUCCESS

def run(e, c):
    return VerifyEmail().verify_email(e, c)

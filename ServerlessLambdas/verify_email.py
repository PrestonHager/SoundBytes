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
            link_id = event["queryStringParameters"]["usr"]
            username = self.database.verify_table.get_item(Key = {"LinkId": link_id})["Item"]["User"]
        except:
            body = {
                "err": "No link id was supplied or it was invalid.",
                "cod": 15
            }
            return self.database.create_response(body, 400)
        # if everything is a success then set Verified to True in user table, and remove link id in verify table.
        self.database.users.update_item(Key = {"Username": username}, AttributeUpdates = {"Verified": {"Value": True}})
        self.database.verify_table.delete_item(Key = {"LinkId": link_id})
        body = {
            "cod": 100
        }
        return self.database.create_response(body, 200)

def run(e, c):
    return VerifyEmail().verify_email(e, c)

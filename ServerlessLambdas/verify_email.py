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
            link_id = event["queryStringParameters"]["usr"]
            username = self.database.verify_table.get_item(Key = {"LinkId": link_id})["Item"]["User"]
        except:
            return RESPONSE_FAILURE
        # if everything is a success then set Verified to True in user table.
        self.database.users.update_item(Key = {"Username": username}, AttributeUpdates = {"Verified": {"Value": True}})
        # remove the link_id from the verify table, and the list of all ids.
        all_links = self.database.verify_table.get_item(Key = {"LinkId": "-1"})["Item"]["AllLinks"]
        all_links.pop(all_links.index(link_id))
        self.database.verify_table.update_item(Key = {"LinkId": "-1"}, AttributeUpdates = {"AllLinks": {"Value": all_links}})
        self.database.verify_table.delete_item(Key = {"LinkId": link_id})
        return RESPONSE_SUCCESS

def run(e, c):
    return VerifyEmail().verify_email(e, c)

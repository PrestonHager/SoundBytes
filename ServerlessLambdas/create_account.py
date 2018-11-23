class CreateAccount:
    def __init__(self):
        # global imports
        global base64, hashlib, json, re, os, DEFAULT_INTRESTS
        import base64, hashlib, json, re, os
        from intrests import DEFAULT_INTRESTS
        # set up the databases
        import databases
        self.database = databases.Databases()

    def verify_json(self, data, params):
        for param in params:
            if param not in data:
                return param
        return False

    """
    Create Account Method: Used by AWS Lambda
    Parameters: event, context
    Output: html response
    """
    def create_account(self, event, context):
        self.database.init_users()
        data = json.loads(event["body"])
        verify = self.verify_json(data, ["username", "password", "email"])
        if verify:
            body = {
                "err": "The '{param}' parameter was not found in the supplied JSON.".format(param=verify),
                "cod": 11
            }
            return self.database.create_response(body, 400)
        try:
            self.database.users.get_item(Key = {"Username": data["username"]})["Item"]
            body = {
                "err": "Username is already taken.",
                "cod": 5
            }
            return self.database.create_response(body, 400)
        except:
            # validate the email string.
            # NOTE: the is a very basic regex and is not the complete offical.
            if not re.match(r"[a-zA-Z0-9\.-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9]+", data["email"]):
                body = {
                    "err": "Invalid email address.",
                    "cod": 10
                }
                return self.database.create_response(body, 400)
            password_hash = base64.b64encode(hashlib.blake2b(bytes(data["password"], "utf-8"), salt=bytes(os.getenv('SALT', "123456abcdef"), "utf-8")).digest())
            user = {"Username": data["username"], "Password": password_hash.decode("utf-8"), "Email": data["email"], "Verified": False, "Intrests": DEFAULT_INTRESTS}
            self.database.users.put_item(Item = user)
            # finally send an email to the user so they can verify it.
            ## TODO: add code for sending email
            body = {
                "cod": 101
            }
            return self.database.create_response(body, 201)

def run(e, c):
    print("Invoked")
    return CreateAccount().create_account(e, c)

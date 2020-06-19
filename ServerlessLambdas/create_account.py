# Define constants for sending emails.
EMAIL_BODY_TEXT = "Welcome to Sound Bytes!\r\n\r\nPlease verify your email by clicking the link below, or pasting it into your web browser.\r\n{link}"
EMAIL_BODY_HTML = "<html><head></head><body><h3>Welcome to Sound Bytes!</h3><p>Please verify your email by clicking the link below, or pasting it into your web browser.</p><p><a href=\"{link}\">{link}</a></p>"

class CreateAccount:
    def __init__(self):
        # global imports
        global base64, boto3, hashlib, json, re, os, DEFAULT_INTRESTS, ClientError
        import base64, boto3, hashlib, json, re, os
        from botocore.exceptions import ClientError
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
            self.database.users.get_item(Key = {"Username": data["username"].lower()})["Item"]
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
            user = {"Username": data["username"].lower(), "Password": password_hash.decode("utf-8"), "Email": data["email"], "Verified": False, "Intrests": DEFAULT_INTRESTS}
            # finally send an email to the user so they can verify it.
            self.database.init_verify_table()
            verify_link = self.database.create_verify_link(data["username"].lower())
            ## TODO: add code for sending email
            client = boto3.client("ses")
            try:
                client.send_email(Destination={"ToAddresses": [data["email"]]}, Message={"Body": {"Html": {"Charset":"utf-8", "Data":EMAIL_BODY_HTML.format(link=verify_link)}, "Text": {"Charset":"utf-8", "Data":EMAIL_BODY_TEXT.format(link=verify_link)}}, "Subject": {"Charset":"utf-8","Data":"Welcome to Sound Bytes!"}}, Source="Sound Bytes Company <sound.bytes.co@gmail.com>")
            except ClientError as e:
                print(e.response["Error"]["Message"])
                body = {
                    "err": "Couldn't send email.\n"+e.response["Error"]["Message"],
                    "cod": 14
                }
                return self.database.create_response(body, 201)
            # if everything is successful, then we may put the user to the database.
            self.database.users.put_item(Item = user)
            body = {
                "cod": 101
            }
            return self.database.create_response(body, 201)

def run(e, c):
    return CreateAccount().create_account(e, c)

class Databases:
    def __init__(self):
        # import anything that might be needed.
        global boto3, json
        import boto3, json
        # set all the default class variables to None
        self.dynamo_db = None
        self.bites = None
        self.users = None
        self.verify_table = None
        self.s3_connection = None
        self.s3_bucket = None
        self.sts_client = None

    def init_sts(self):
        self.sts_client = boto3.client('sts')
        return True

    def _init_dynamodb(self):
        # set the dynamo_db and dynamo_table variables to their
        self.dynamo_db = boto3.resource("dynamodb", region_name="us-east-1")
        # return True from the process
        return True

    def init_bites_db(self):
        self._init_dynamodb()
        # correct resources.
        self.bites = self.dynamo_db.Table("soundbytes-bites-metadata")
        # return True from the process.
        return True

    def init_users(self):
        self._init_dynamodb()
        # set to the user dynamodb table.
        self.users = self.dynamo_db.Table("soundbytes-users")
        # return True from the proccess
        return True

    def init_verify_table(self):
        self._init_dynamodb()
        # set to the verify dynamodb table.
        self.verify_table = self.dynamo_db.Table("soundbytes-verify")
        # return True from the proccess
        return True

    def init_s3(self):
        # set the s3_connection to a client connection to s3 using boto3.
        self.s3_connection = boto3.client('s3')
        # return True from the process.
        return True

    def upload_s3(self, file_stream, key):
        # upload a file obj/stream to the s3 bucket.
        try:
            self.s3_connection.upload_fileobj(file_stream, "soundbytes-bites", key)
        except Exception as err:
            return err
        # return True from the process.
        return True

    def create_response(self, body, code):
        # this will create an html readable response with a code.
        return {
            "statusCode": code,
            "body": json.dumps(body)
        }

    def create_verify_link(self, username):
        import random, secrets
        from branca import Branca
        # all_links = self.verify_table.get_item(Key = {"LinkId": "-1"})["Item"]["AllLinks"]
        key = "%016x" % random.randrange(16**16)
        # all_links.append(verify_link)
        # self.verify_table.update_item(Key = {"LinkId": "-1"}, AttributeUpdates = {"AllLinks": {"Value": all_links}})
        key = secrets.token_hex(32)
        branca = Branca(key)
        verify_link = branca.encode(username + ":" + key)
        self.verify_table.put_item(Item = {"LinkId": verify_link, "User": username, "BrancaKey": key})
        return "https://api.soundbytes.xyz/dev/verify/" + verify_link

    def create_unsubscribe_link(self, email):
        from urllib import quote_plus
        return "https://api.soundbytes.xyz/dev/unsubscribe?email=" + quote_plus(email)

    def get_credentials(self, session_name, resource_name=None):
        if resource_name == None:
            session_policy = {}
        else:
            session_policy = {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Action": "s3:PutObject",
                        "Resource": resource_name
                    }
                ]
            }
        response = self.client.assume_role(
            RoleArn="arn:aws:iam::105554980019:role/soundbytes-s3",
            RoleSessionName=session_name,
            Policy=json.dumps(session_policy)
        )
        credentials = response["Credentials"]
        if credentials != None:
            credentials["Expiration"] = credentials["Expiration"].isoformat()
            return credentials
        else:
            return False

    def send_email(self, to_address, template, subject, **kwargs):
        import smtplib, ssl, os
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        smtp_server = "smtp.zoho.com"
        port = 587
        # Create a secure SSL context
        context = ssl.create_default_context()
        sender_email = "support@soundbytes.xyz"
        password = os.getenv("APP_PASSWORD", "")
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = sender_email
        message["To"] = to_address
        message["List-Unsubscribe"] = "<mailto:unsubscribe@soundbytes.xyz?subject=Unsubscribe>, <http://soundbytes.xyz/unsubscribe>"
        # message_header = "To: {to}\nFrom: \"Sound Bytes\" <{sender}>\nList-Unsubscribe: <mailto:unsubscribe@soundbytes.xyz?subject=Unsubscribe>, <http://soundbytes.xyz/unsubscribe>\nSubject: Welcome to SoundBytes".format(to=to_address, sender=sender_email)
        with open("email_templates/"+template+'.txt', 'r') as f_in:
            text_template = f_in.read()
            text = MIMEText(text_template.format(**kwargs), "plain")
            message.attach(text)
        with open("email_templates/"+template+'.html', 'r') as f_in:
            html_template = f_in.read()
            html = MIMEText(html_template.format(**kwargs), "html")
            message.attach(html)
        # Try to log in to server and send email
        try:
            server = smtplib.SMTP(smtp_server, port)
            server.ehlo() # Can be omitted
            server.starttls(context=context) # Secure the connection
            server.ehlo() # Can be omitted
            server.login(sender_email, password)
            # Send email here
            server.sendmail(sender_email, to_address, message.as_string())
        except Exception as e:
            import traceback
            print(traceback.format_exc())
        finally:
            server.quit()

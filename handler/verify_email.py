class VerifyEmail:
    def __init__(self):
        # set up the databases
        import databases
        self.database = databases.Databases()

    def verify_email(self, event, context):
        body = {
            "cod": 100
        }
        return self.database.create_response(body, 200)

def run(e, c):
    return VerifyEmail().verify_email(e, c)

class Authorizer:
    def __init__(self):
        # global imports
        global Branca, json, os
        import json, os
        from branca import Branca
        # set up the databases
        import databases
        self.database = databases.Databases()

    def authorize(self, event, context):
        self.database.init_users()
        if 'authorizationToken' in event:
            token = event['authorizationToken']
        else:
            return self.forbidden()
        # Decode the Branca token
        branca_token = Branca(os.getenv('BRANCA_KEY', "d8b647974af437bdf761099cec8d3e5ac263037d02c8ad8498efc7eef27e0a33"))
        decoded_token = branca_token.decode(token).decode('utf-8')
        if ":" in decoded_token:
            username, auth_token = decoded_token.split(':')
            print(username, auth_token)
        else:
            return self.forbidden()
        user_query = self.database.users.get_item(Key = {"Username": username.lower()})
        if "Item" in user_query:
            user = user_query["Item"]
        else:
            return self.generatePolicy(user, 'Deny', event['methodArn'])
        if auth_token == user["AuthToken"]:
            return self.generatePolicy(user, 'Allow', event['methodArn'])
        else:
            return self.generatePolicy(user, 'Deny', event['methodArn'])

    def generatePolicy(self, user, effect=None, resource=None):
        authResponse = {}
        principalId = user["Username"]
        authResponse['principalId'] = principalId
        if effect != None and resource != None:
            policyDocument = {}
            policyDocument['Version'] = '2012-10-17'
            policyDocument['Statement'] = []
            statementOne = {}
            statementOne['Action'] = 'execute-api:Invoke'
            statementOne['Effect'] = effect
            statementOne['Resource'] = resource
            policyDocument['Statement'].append(statementOne)
            authResponse['policyDocument'] = policyDocument

        authResponse['context'] = {
            # include additional arguments to the authorizer here
        }
        return authResponse

    def forbidden(self):
        response = {
            "code": 401,
            "body": json.dumps({
                "message": "User forbidden."
            })
        }
        return response

def run(e, c):
    return Authorizer().authorize(e, c)

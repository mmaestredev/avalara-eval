from avalara import AvataxClient

def init():
    try:
        client = AvataxClient('my test app', 'ver 0.0', 'my test machine',  'sandbox')
        client = client.add_credentials('miguel.m@servicepad.com', 'mamp10625652')
        res = (client.ping()).json()

        if (res["authenticated"] == False):
            raise Exception("Client authentication failed.")
        
        return client
    except Exception as E:
        print(E)
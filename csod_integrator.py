from flask import Flask, request
import requests
from dataParser import data_parser


# tells whether we have received the access token or not
INITIATED = False

APPICATION_NAME = ""

CLIENT_ID = ""

CLIENT_SECRETE = ""

ACCESS_TOKEN = ""

ACCESS_TOKEN_VALID_TILL = ""

def fire_Access_Request( applicationName , clientID , client_secrete ):

    #forming an access token url
    url =  "https://" + applicationName   + ".csod.com/services/api/oauth2/token"

    # - H 'Content-Type: application/json' \
    # - H 'cache-control: no-cache'
    header = {}
    header["Content-Type"] = "application/json"
    header["cache-control"] = "no-cache"

    
    # "grantType": "client_credentials",
    # "scope": "all"
    body = {}
    body["clientId"] = clientID
    body["clientSecret"] =client_secrete
    body["grantType"] = "client_credentials"
    body["scope"] = "all"

    output = requests.post( url , json = body, headers = header )
    ACCESS_TOKEN = (output.json())["access_token"]
    print("Fire Access query :" + ACCESS_TOKEN)
    return ACCESS_TOKEN


app  = Flask(__name__)

@app.route("/")
def welcome():
    return "go to /middleware/help"

@app.route("/middleware")
def init():
    APPICATION_NAME  = request.args.get('application_Name')
    CLIENT_ID = request.args.get( 'client_ID')
    CLIENT_SECRETE = request.args.get( 'client_secrete')

    ACCESS_TOKEN = fire_Access_Request(APPICATION_NAME , CLIENT_ID , CLIENT_SECRETE )
    INITIATED = True
    return (ACCESS_TOKEN)



@app.route("/middleware/help")
def help():
    return "<H1> API information is as below : </H1>" \
           "<p> for access token retrival :  http://DOMAIN_NAME:5000//middleware "\
           "with query parameter as application_Name , 'client_ID' ,'client_secrete' </p>"\
           "<p> fr OU related information :  http://DOMAIN_NAME:5000//middleware/OU"\
           "with query parameter as OuType , application_Name , 'client_ID' ,'client_secrete' </p>"\
           .format("your domain name", "your domain name")\


@app.route("/middleware/OU")
def getOU():
    if INITIATED == False:
        ACCESS_TOKEN = init()
   
    #Dynamically generating the url 
    application_name = request.args.get ("application_Name")
    url =  "https://"+application_name+".csod.com/services/api/OrgUnits/OU"
    print(url)



    header = {}
    header ["Authorization"] = "Bearer {}".format(ACCESS_TOKEN)
    header ["cache-control"] = "no-cache"

    body = {}
    body["OuType"] = request.args.get ("OuType")

    print("Bearer {}  ".format(ACCESS_TOKEN) + body["OuType"])

    output = requests.get( url , params=body, headers = header)

    print(output.status_code)

    if(output.status_code==200):
        return data_parser(output)
    else:
        return "No , it did not work"


# application start
if __name__ == '__main__':
    app.run(debug=False)



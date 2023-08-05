import json
import time
from urllib.parse import urlencode
import jwt
import requests

class AdobeIO:
    def __init__(self, ORG_ID, ACCNT_ID,API_KEY,IMS_HOST,PRIVATE_KEY_PATH,CLIENT_SECRET):
        self.ORG_ID = ORG_ID
        self.ACCNT_ID = ACCNT_ID
        self.API_KEY =API_KEY
        self.IMS_HOST=IMS_HOST
        self.PRIVATE_KEY_PATH = PRIVATE_KEY_PATH
        self.CLIENT_SECRET = CLIENT_SECRET
        self.jwt_token = ""
        self.access_token=""

    def generate_jwt(self,API_PATH):
        #expiry time as 24 hours
        expiry_time_jwt = int(time.time()) + 60 * 60 * 24
        # create payload
        payload = {
            'exp': expiry_time_jwt,
            'iss': self.ORG_ID,
            'sub': self.ACCNT_ID,
            API_PATH: True,
            'aud': self.IMS_HOST + "/c/" + self.API_KEY
        }
        # read the private key we will use to sign the JWT.
        priv_key_file = open(self.PRIVATE_KEY_PATH)
        priv_key = priv_key_file.read()
        priv_key_file.close()
        # create JSON Web Token, signing it with the private key.
        jwt_token = jwt.encode(payload, priv_key, algorithm='RS256')
        self.jwt_token = jwt_token
        return jwt_token

    def generate_access_token(self):
        access_token = ''

        # Final URL for access-token generation API end-point
        accesstoken_url =  self.IMS_HOST + "/ims/exchange/jwt/"

        accesstoken_headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Cache-Control": "no-cache"
        }

        accesstoken_body_credentials = {
            "client_id": self.API_KEY,
            "client_secret": self.CLIENT_SECRET,
            "jwt_token": self.jwt_token
        }

        accesstoken_body = urlencode(accesstoken_body_credentials)
        # send http request
        print(accesstoken_body)
        print(accesstoken_url)
        res = requests.post(accesstoken_url, headers=accesstoken_headers, data=accesstoken_body)

        if res.status_code == 200:
            # extract token
            access_token = json.loads(res.text)['access_token']
        self.access_token = access_token
        return access_token

class AAM(AdobeIO):
    def __init__(self, ORG_ID, ACCNT_ID,API_KEY,IMS_HOST,PRIVATE_KEY_PATH,CLIENT_SECRET):
        AdobeIO.__init__(self, ORG_ID, ACCNT_ID,API_KEY,IMS_HOST,PRIVATE_KEY_PATH,CLIENT_SECRET)
        self.datasourceendpoint = "https://api.demdex.com/v1/datasources/"
        self.traitsendpoint = "https://api.demdex.com/v1/traits/"
        self.traitfoldersendpoint = "https://api.demdex.com/v1/folders/traits/"
        self.segmentsendpoint = "https://api.demdex.com/v1/segments/"
        self.segmentfoldersendpoint = "https://api.demdex.com/v1/folders/segments/"


    def auth_header(self):
        return {
            "x-api-key":self.API_KEY,
            "content-type": "application/json",
            "accept": "application/json",
            "Authorization": "Bearer "+self.access_token
        }

    def get_datasource(self,params):
        return requests.get(self.datasourceendpoint,headers=self.auth_header(),params=params)

    def get_traits(self,params=None):
        return requests.get(self.traitsendpoint,headers=self.auth_header(),params=params)

    def get_segments(self,params=None):
        return requests.get(self.segmentsendpoint,headers=self.auth_header(),params=params)

    def get_segment_folders(self,params=None):
        return requests.get(self.segmentfoldersendpoint,headers=self.auth_header(),params=params)

    def get_trait_folders(self,params=None):
        return requests.get(self.traitfoldersendpoint,headers=self.auth_header(),params=params)
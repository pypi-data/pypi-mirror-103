#Only run this once
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

import json
import urllib
import  urllib.parse
#import pandas as pd
import getpass
from requests.auth import HTTPBasicAuth

class Ikewai:

    def __init__(self, endpoint='https://ikeauth.its.hawaii.edu', token_url='https://ikewai.its.hawaii.edu:8888/login', token='', username='guest'):
      self.endpoint = endpoint
      self.token_url = token_url
      self.token = token
      self.username = username

    def login(self):
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        res = requests.post(self.token_url+'?', auth=HTTPBasicAuth(self.username, getpass.getpass()), verify=False)
        resp=json.loads(res.content)
        if 'error' in resp:
            print('Login Error- please check your username and password combination and try again')

        else:
            self.token = resp['access_token']
            expiration_minutes = (resp['expires_in']/60)
            print('Login  Successful - token has been set and will be valid for '+str(int(expiration_minutes))+' minutes. You can now access Ike Wai data.')
        return

    # Search IkeWai metadata with a query.
    # Limit is the number of result objects to retrun
    # Offset is the number of objects to skip
    # Limit and Offset can be used to paginate results
    # - or you can set limit to a very large number to get all the results at once (depending on the query this can be
    # a lot of information returned)
    def searchMetadata(self, query="", limit=10, offset=0):
        safe_query = urllib.parse.quote(query.encode('utf8'))
        headers = {
            'authorization': "Bearer " + self.token,
            'content-type': "application/json",
        }
        res = requests.get(self.endpoint+'/meta/v2/data?q='+safe_query+'&limit='+str(limit)+'&offset='+str(offset), headers=headers)
        resp = json.loads(res.content)
        if 'result' in resp:
            return resp['result']
        else:
            return resp

    # Given a water quality site id download the csv file of data from waterqualitydata.us
    def downloadWaterQualityData(id):
        res = requests.get(' https://www.waterqualitydata.us/data/Result/search?siteid='+id+'&mimeType=csv')
        return res.content

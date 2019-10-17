import requests
import json

class SalesforceConnection:
    def __init__(self, username, password, token, consumer_key, consumer_secret, baseUrl="https://login.salesforce.com", api_version="v47.0"):
        self.params = {
            "grant_type": "password",
            "client_id": consumer_key,
            "client_secret": consumer_secret,
            "username": username,
            "password": password + token
        }
        self.api_version = api_version
        self.access_token, self.instance_url = self.__retrieveToken(self.params, baseUrl)
        print(self.access_token)
        
    def __retrieveToken(self, params, url):
        req = requests.post(url+"/services/oauth2/token", params=params)
        access_token = req.json().get("access_token")
        instance_url = req.json().get("instance_url")
        return (access_token, instance_url)

    def __sf_api_call(self,action, parameters = {}, method = 'get', data = {}):
        """
        Helper function to make calls to Salesforce REST API.
        Parameters: action (the URL), URL params, method (get, post or patch), data for POST/PATCH.
        """
        headers = {
            'Content-type': 'application/json',
            'Accept-Encoding': 'gzip',
            'Authorization': 'Bearer %s' % self.access_token
        }
        
        if method == 'get':
            req = requests.request(method, self.instance_url+action, headers=headers, params=parameters, timeout=30)
        elif method in ['post', 'patch']:
            req = requests.request(method, self.instance_url+action, headers=headers, json=data, params=parameters, timeout=10)
        else:
            raise ValueError('Method should be get or post or patch.')
        print('Debug: API %s call: %s' % (method, req.url) )
        if req.status_code < 300:
            if method=='patch':
                return None
            else:
                return req.json()
        else:
            raise Exception('API error when calling %s : %s' % (req.url, req.content))
        
    def create_lead(self, data):
        action = "/services/data/"+self.api_version+"/sobjects/Lead/"
        method = "post"
        params = {}
        data = data

        return self.__sf_api_call(action, params, method, data)
        
    def rest_versions(self):
        action = "/services/data/"
        print(json.dumps(self.__sf_api_call(action, None), indent=2))
        
    def query(self):
        print(json.dumps(self.__sf_api_call('/services/data/v39.0/query/', {
            'q': 'SELECT Account.Name, Name, CloseDate from Opportunity LIMIT 10'
            }), indent=2))

sc = SalesforceConnection("miguel.tavarez@badob.com", "Birchman.2019", "1w1Id4cUMxpoXVusLbZNwooG", "3MVG9HxRZv05HarQ5An2NKjdMjE1eBEfjBj9WSC4YvrYDFa7bFVcJ.fjkRrqaABVy.i8namQdEr9iPY3ZpcFq", "3F8EE6CE2525CA9EA0040C21A513091C6CEB53948FC3BAC51937873A87823F23")

params = {
    "RecordTypeId": "0120Y0000001fI9QAI",
    "LastName" : "Hola",
    "Status" : "Validado",
}

print(json.dumps(sc.create_lead(params), indent=2))

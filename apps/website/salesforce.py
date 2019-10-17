import requests

class Salesforce:
        def __init__(self, username, password, security_token, consumer_key, client_secret, instance_url="https://eu18.salesforce.com"):
                self.consumer_key = consumer_key
                self.client_secret = client_secret
                self.username = username
                self.password = password
                self.security_token = security_token
                self.instance_url = instance_url
                self.login_url = self.instance_url + "/services/oauth2/token"
                self.params = self.__createParams(username, password, security_token, consumer_key, client_secret)
                self.access_token = self.__connect(self.params);
                print("Connection established successfully to:")
                print("Access Token:", self.access_token)
                print("Instance URL", self.instance_url)

        def __createParams(self, username, password, security_token, consumer_key, client_secret):
                params = {
                "grant_type": "password",
                "client_id": consumer_key, 
                "client_secret": client_secret, 
                "username": username ,
                "password": password+security_token,
                "redirect_uri": "https://localhost/"
                }
                print(params)
                return params;

        def __connect(self, params):
                r = requests.post(self.login_url, params=params)
                print(r.json())
                access_token = r.json().get("access_token")
                return access_token;

        def createLead(self, fields):
                pass

username = 'miguel.tavarez@badob.com'
password = 'Birchman.2019'
token='3bPIdOU9bKd8TJQc7sZUXcg88'
consumer_key = '3MVG9HxRZv05HarQ5An2NKjdMjPsdxIekmtOXiFB3H0WlFHh.4E_WxZPXj._v.NZ6RyCZmrQ1PuH.lCRoOD1D'
client_secret = '487DEFA936A1A5DD2A010F96DACF1D4F118C547A6476C775A95FEF9EEB8C5F00'


s = Salesforce(username, password, token, consumer_key, client_secret)

from django.shortcuts import render
from website.models import WebSettings
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from PIL import Image
import base64
import face_recognition
import cv2 #on local switch to cv2 only.
import time
import os
import io
import string
import random
import numpy as np
#-------------------CONEXION SALESFORCE---------------------

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


#----------------------------------------

def randomString(stringLength=10):
        """Generate a random string of fixed length """
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(stringLength))

def index(request):
        active_settings = WebSettings.objects.filter(is_active=True)
        
        if active_settings.count() is not 1:
                pass #throw exception
        
        active_settings = active_settings.get();
        
        
        return render(request, 'index.html', context=model_to_dict(active_settings))

def landing_page(request):
        return render(request, 'landing_page.html')

@csrf_exempt
def create_lead(request):
        sc = SalesforceConnection("miguel.tavarez@badob.com", "Birchman.2019", "1w1Id4cUMxpoXVusLbZNwooG", "3MVG9HxRZv05HarQ5An2NKjdMjE1eBEfjBj9WSC4YvrYDFa7bFVcJ.fjkRrqaABVy.i8namQdEr9iPY3ZpcFq", "3F8EE6CE2525CA9EA0040C21A513091C6CEB53948FC3BAC51937873A87823F23")

        params = {
                "RecordTypeId": "0120Y0000001fI9QAI",
                "Status" : "Validado",
                "FirstName": request.POST.get("first_name"),
                "LastName": request.POST.get("last_name") + request.POST.get("second_last_name"),
                "Email": request.POST.get("email"),
                "Phone": request.POST.get("phone"),
                "Marital_Status__c": request.POST.get("estado_civil"),
                "Salutation": "Mr" if request.POST.get("sexo") is "Masculino" else "Mrs",
                "Birth_Date__c": request.POST.get("birth_year") +'-'+ request.POST.get("birth_month") +'-'+ request.POST.get("birth_date"),
                "Ciudadania_US__c": request.POST.get("ciudadania"),
                "Direccion__c": request.POST.get("direccion"),
                "Tipo_documento__c": request.POST.get("documentType"),
                "Numero_documento__c": request.POST.get("documentNumber"),
                "Residente_RD__c": request.POST.get("residencia"),
                "Producto__c": request.POST.get("productType"),
                "Necesidad__c": request.POST.get("necesidad"),
                "Imagen__c": '<img alt="<image_Name>" src="' + request.POST.get("image__c") + '"></img>'
        }

        print(params);
        
        sc.create_lead(params)
        return JsonResponse({})
        
@csrf_exempt
def validate_photo(request):
        print('======================START=================' )
        active_settings = WebSettings.objects.filter(is_active=True)
        card = base64.b64decode(request.POST.get("cardPhoto").partition(',')[2])
        cam = base64.b64decode(request.POST.get("camFrame").partition(',')[2])
        match = False
        
        random_string = randomString(10);
        card_filename = random_string + '_card.jpeg'
        with open('tmp/'+card_filename, 'wb') as f:
                f.write(card)
                
        cam_filename = random_string + '_cam.jpeg'
        with open('tmp/'+cam_filename, 'wb') as f:
                f.write(cam)
                
        print(os.getcwd())
        
        card = cv2.imread('tmp/'+card_filename)
        card_gray = cv2.cvtColor(card, cv2.COLOR_BGR2GRAY)

        card3c = np.zeros_like(card)
        card3c[:,:,0] = card_gray
        card3c[:,:,1] = card_gray
        card3c[:,:,2] = card_gray
        
        cam = cv2.imread('tmp/'+cam_filename)
        cam_gray = cv2.cvtColor(cam, cv2.COLOR_BGR2GRAY)

        cam3c = np.zeros_like(cam)
        cam3c[:,:,0] = cam_gray
        cam3c[:,:,1] = cam_gray
        cam3c[:,:,2] = cam_gray
        
        
        biden_encodings = face_recognition.face_encodings(card3c, num_jitters=1)
        unknown_encodings = face_recognition.face_encodings(cam3c, num_jitters=1)

        print('biden :: ' + str(biden_encodings))
        print('unknown_encodings :: ' + str(unknown_encodings))
        
        if len(biden_encodings) > 0 and len(unknown_encodings) > 0:
                results = face_recognition.compare_faces([biden_encodings[0]], unknown_encodings[0], 0.7)
                distance = face_recognition.face_distance([biden_encodings[0]], unknown_encodings[0])
                print('dist: ' + str(distance))
                match = (results[0] is np.True_)

        print(match)
        if match:
                modal_title = active_settings[0].success_message_title
                modal_message = active_settings[0].success_message_body
                

        else:
                modal_title = active_settings[0].failure_message_title
                modal_message = active_settings[0].failure_message_body
        
        os.remove('tmp/'+card_filename)
        os.remove('tmp/'+cam_filename)
        print('======================END=================' )
        return JsonResponse({'match' : match})

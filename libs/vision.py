from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import base64
import apps.api.face_recognition as face_recognition
import cv2 #on local switch to cv2 only.
import os
import io
import string
import random
import numpy as np
from apps.api.views import randomString

class Vision:
        @csrf_exempt
        def validate_photo(request):

                card = base64.b64decode(request.POST.get("cardPhoto").partition(',')[2])
                cam = base64.b64decode(request.POST.get("camFrame").partition(',')[2])
                match = False
        
                random_string = randomString(10)
                card_filename = random_string + '_card.jpeg'
                with open('tmp/'+card_filename, 'wb') as f:
                        f.write(card)
                
                cam_filename = random_string + '_cam.jpeg'
                with open('tmp/'+cam_filename, 'wb') as f:
                        f.write(cam)
        
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
        
                if len(biden_encodings) > 0 and len(unknown_encodings) > 0:
                        results = face_recognition.compare_faces([biden_encodings[0]], unknown_encodings[0], 0.7)
                        distance = face_recognition.face_distance([biden_encodings[0]], unknown_encodings[0])
                        match = (results[0] is np.True_)
        
                os.remove('tmp/'+card_filename)
                os.remove('tmp/'+cam_filename)
                return JsonResponse({'match' : match})

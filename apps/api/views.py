from django.shortcuts import render
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from PIL import Image
import base64
import face_recognition
import cv2 #on local switch to cv2 only.
import os
import io
import string
import random
import numpy as np
from libs import SalesforceConnection

# Create your views here.
#class utilities:
def randomString(stringLength=10): #utilities
        """Generate a random string of fixed length """
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(stringLength)) 

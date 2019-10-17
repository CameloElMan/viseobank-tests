from django.urls import path
from . import views
from libs import vision

urlpatterns = [
	path('app/ajax/validate_photo/', vision.Vision.validate_photo, name='validate_photo'),
]
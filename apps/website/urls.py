from django.urls import path
from . import views

urlpatterns = [
	path('', views.landing_page, name='landing_page'),
	path('app/', views.index, name='index'),
	# path('app/ajax/validate_photo/', views.validate_photo, name='validate_photo'),
    path('app/ajax/create_lead/', views.create_lead, name='create_lead'),
]

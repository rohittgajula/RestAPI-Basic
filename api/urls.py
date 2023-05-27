from django.urls import path

from app.views import *

urlpatterns = [
    path('people/', people),
    path('login/', login),
    path('personAPI/', PersonAPI.as_view()),        # class based views
    path('loginAPI/', loginAPI.as_view()),
]


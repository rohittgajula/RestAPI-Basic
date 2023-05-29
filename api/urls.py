from django.urls import path, include

from app import views

# ----------------- 
# for ViewSet we need to import as router.

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('person', views.PeopleViewSet, basename='person')
urlpatterns = router.urls

# ----------------------------------

urlpatterns = [
    path('', include(router.urls)),                 # for model viewset.
    path('register/', views.RegisterAPI.as_view()),     # adding .as_view() -- because we are using APIview {class based.}
    path('people/', views.people),
    path('login/', views.login),
    path('personAPI/', views.PersonAPI.as_view()),        # class based views
    path('loginapi/', views.loginAPI.as_view()),
    path('loginAPI/', views.LoginAPI.as_view()),
]


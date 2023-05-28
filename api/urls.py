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
    path('people/', views.people),
    path('login/', views.login),
    path('personAPI/', views.PersonAPI.as_view()),        # class based views
    path('loginAPI/', views.loginAPI.as_view()),
]


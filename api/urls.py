from django.urls import path
from .views import CreatePsychoTest

urlpatterns = [
    path('create_psycho_test/', CreatePsychoTest.as_view(), name='create-psycho-test')
]

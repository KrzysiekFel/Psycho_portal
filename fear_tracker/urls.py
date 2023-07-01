from django.urls import path
from .views import fear_tracker

urlpatterns = [
    path('', fear_tracker, name='fear-tracker'),
]

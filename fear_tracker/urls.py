from django.urls import path
from .views import fear_tracker, plot_fear, FearCreateView

urlpatterns = [
    path('', fear_tracker, name='fear-tracker'),
    path('new/', FearCreateView.as_view(), name='fear-create'),
    path('plot/', plot_fear, name='fear-plot')
]

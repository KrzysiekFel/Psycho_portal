from django.urls import path
from .views import fear_tracker, YourChartView, FearCreateView

urlpatterns = [
    path('', fear_tracker, name='fear-tracker'),
    path('new/', FearCreateView.as_view(), name='fear-create'),
    path('plot/', YourChartView.as_view(), name='fear-plot')
]

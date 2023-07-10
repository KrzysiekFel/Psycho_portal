from django.urls import path
from .views import YourChartView, FearCreateView

urlpatterns = [
    path('', YourChartView.as_view(), name='fear-tracker'),
    path('new/', FearCreateView.as_view(), name='fear-create'),
    #path('plot/', YourChartView.as_view(), name='fear-plot')
]

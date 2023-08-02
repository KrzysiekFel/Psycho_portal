from django.urls import path
from .views import YourChartView, FearCreateView, FearListView, FearDeleteView

urlpatterns = [
    path('', YourChartView.as_view(), name='fear-tracker'),
    path('new/', FearCreateView.as_view(), name='fear-create'),
    path('list/', FearListView.as_view(), name='fear-list'),
    path('delete/<int:pk>', FearDeleteView.as_view(), name='fear-delete')
]

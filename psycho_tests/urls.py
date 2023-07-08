from django.urls import path
from .views import TestResultView, CreateTestView, PsychoTestsListView, TestFillView

urlpatterns = [
    path('', PsychoTestsListView.as_view(), name='psycho-tests'),
    path('create/', CreateTestView.as_view(), name='create-test'),
    path('test/<int:test_id>', TestFillView.as_view(), name='test-detail'),
    path('result/<int:result_id>/', TestResultView.as_view(), name='test-result'),
]

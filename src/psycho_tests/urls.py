from django.urls import path
from .views import (
    TestResultView,
    CreateTestView,
    PsychoTestsListView,
    TestFillView,
    AllTestResultView,
    DeleteTestView,
    PendingPsychoTestListView,
    publish_test,
)

urlpatterns = [
    path("", PsychoTestsListView.as_view(), name="psycho-tests"),
    path("create/", CreateTestView.as_view(), name="create-test"),
    path("test/<int:test_id>", TestFillView.as_view(), name="test-detail"),
    path("result/<int:result_id>/", TestResultView.as_view(), name="test-result"),
    path("results/", AllTestResultView.as_view(), name="all-test-results"),
    path("delete_test/<int:pk>/", DeleteTestView.as_view(), name="delete-test"),
    path("tests_to_publish/", PendingPsychoTestListView.as_view(), name="tests-to-publish"),
    path("publish/<int:test_id>/", publish_test, name="publish-test"),
]

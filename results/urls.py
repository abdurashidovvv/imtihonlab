from django.urls import path
from .views import UserTestResultAPIView, UserAllResultsAPIView

urlpatterns = [
    path(
        'results/<int:test_id>/',
        UserTestResultAPIView.as_view(),
        name='user-test-result'
    ),
    path(
        'results/',
        UserAllResultsAPIView.as_view(),
        name='user-all-results'
    ),
]

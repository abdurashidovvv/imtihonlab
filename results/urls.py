from django.urls import path
from .views import UserTestResultAPIView

urlpatterns = [
    path(
        'results/<int:test_id>/',
        UserTestResultAPIView.as_view(),
        name='user-test-result'
    ),
]

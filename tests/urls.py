from django.urls import path
from .views import TestCreateView, TestListView, TestDetailView

urlpatterns = [
    path("tests/create/", TestCreateView.as_view(), name="test-create"),
    path("tests/", TestListView.as_view(), name="test-list"),
    path("tests/<int:id>/", TestDetailView.as_view(), name="test-detail"),
]

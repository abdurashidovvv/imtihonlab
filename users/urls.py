from django.urls import path
from .views import UserRegisterView, UserListView

urlpatterns = [
    path('auth/register/', UserRegisterView.as_view(), name='telegram_auth'),
    path('users/', UserListView.as_view(), name='user_list'),
]
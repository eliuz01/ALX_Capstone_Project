from django.urls import path
from .views import RegisterView, LoginView, ProfileUserRetrieveUpdateView, CustomUserListView, \
CustomUserRetrieveUpdateDestroyView
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('users/', CustomUserListView.as_view(), name='user-list'),
    path('profile/', ProfileUserRetrieveUpdateView.as_view(), name='profile-detail'),
    path('users/detail/<int:student_id>/', CustomUserRetrieveUpdateDestroyView.as_view(), name='user-detail'),
]

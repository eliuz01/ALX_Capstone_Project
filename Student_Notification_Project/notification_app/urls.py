from django.urls import path
from .views import RegisterView, LoginView, ProfileUserRetrieveUpdateView, CustomUserListView, \
CustomUserRetrieveUpdateDestroyView, BusListCreateAPIView, BusRetrieveUpdateDestroyAPIView
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('users/', CustomUserListView.as_view(), name='user-list'),
    path('profile/', ProfileUserRetrieveUpdateView.as_view(), name='profile-detail'),
    path('users/detail/<int:student_id>/', CustomUserRetrieveUpdateDestroyView.as_view(), name='user-detail'),
    path('buses/', BusListCreateAPIView.as_view(), name='bus-list-create'),
    path('buses/<str:pk>/', BusRetrieveUpdateDestroyAPIView.as_view(), name='bus-retrieve-update-destroy'),
]

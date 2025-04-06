from django.urls import path
from .views import RegisterView, LoginView, ProfileUserRetrieveUpdateView, CustomUserListView, \
CustomUserRetrieveUpdateDestroyView, BusListCreateAPIView, BusRetrieveUpdateDestroyAPIView, SmartcardRetrieveUpdateDestroyAPIView, \
SmartcardCreateAPIView, DriverRetrieveUpdateDestroyAPIView, DriverCreateAPIView
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('users/', CustomUserListView.as_view(), name='user-list'),
    path('profile/', ProfileUserRetrieveUpdateView.as_view(), name='profile-detail'),
    path('users/detail/<int:student_id>/', CustomUserRetrieveUpdateDestroyView.as_view(), name='user-detail'),
    path('buses/', BusListCreateAPIView.as_view(), name='bus-list-create'),
    path('buses/<str:pk>/', BusRetrieveUpdateDestroyAPIView.as_view(), name='bus-retrieve-update-destroy'),
    path('smartcards/', SmartcardCreateAPIView.as_view(), name='smartcard-create'),
    path('smartcards/<int:pk>/', SmartcardRetrieveUpdateDestroyAPIView.as_view(), name='smartcard-retrieve-update-destroy'),
    path('drivers/', DriverCreateAPIView.as_view(), name='driver-create'),
    path('drivers/<int:pk>/', DriverRetrieveUpdateDestroyAPIView.as_view(), name='driver-retrieve-update-destroy'),
]

from django.urls import path
from .views import LoginView, InvitationCreateAPIView, InvitationAcceptAPIView, InvitationCancelAPIView
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
# )

urlpatterns = [
    path('login/', LoginView.as_view()),
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('invite/', InvitationCreateAPIView.as_view(), name='create_invitation'),
    path('accept/<uuid:token>/', InvitationAcceptAPIView.as_view(), name='accept_invitation'),
    path('cancel/<uuid:token>/', InvitationCancelAPIView.as_view(), name='cancel_invitation'),
]

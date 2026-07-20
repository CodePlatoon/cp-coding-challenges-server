from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from core.views import RegisterView, ChallengeListView, SaveSubmissionView, RunCodeView, UserCompleteView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/register/', RegisterView.as_view(), name='register'),
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/challenges/', ChallengeListView.as_view(), name='challenge_list'),
    path('api/challenges/<uuid:pk>/save/', SaveSubmissionView.as_view(), name='challenge_save'),
    path('api/challenges/<uuid:pk>/run/', RunCodeView.as_view(), name='challenge_run'),
    path('api/user/complete/', UserCompleteView.as_view(), name='user_complete'),
]

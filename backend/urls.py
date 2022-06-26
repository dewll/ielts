from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import (RegistrationView, SigninView,ProfileView, 
                    CheckEmailView,PasswordResetView,PasswordConfirmView,
                    UploadView, AudioView,SkillVerifyView,SkillView)

app_name = 'back'

urlpatterns = [
    path('',RegistrationView.as_view(), name ='registration'),
    path('signin/',SigninView.as_view(), name ='signin'),
    path('upload/',UploadView.as_view(), name ='upload'),
    path('audio/',AudioView.as_view(), name ='audio'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('home/',SkillVerifyView.as_view(), name ='home'),
    path('payment/',SkillView.as_view(), name ='payment'),
    path('check_email/', CheckEmailView.as_view(), name='check_email'),
    path('password_reset/<uidb64>/<token>/', PasswordResetView.as_view(), name = 'password_reset'),
    path('password_confirm/', PasswordConfirmView.as_view(), name='password_confirm'),
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                                document_root=settings.MEDIA_ROOT)


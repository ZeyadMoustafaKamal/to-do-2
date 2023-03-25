from django.urls import path
from . import views
urlpatterns = [
    path('signup', views.SignUp.as_view(), name='signup'),
    path('login', views.Login.as_view(), name='login'),
    path('logout', views.logout, name='logout'),
    path('verify/<code>', views.Verify.as_view(), name='verify'),
    path('verify-your-email/<code>', views.VerifyEmail.as_view(), name='verify_email')
]
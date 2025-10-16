
from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('forgot_password_request/', views.forgot_password_request, name='forgot_password_request'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('logout/', views.logout_user, name='logout'),
]
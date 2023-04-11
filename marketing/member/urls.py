from django.urls import path
from . import views
app_name = 'member'

urlpatterns = [
    path('',views.UserLogin,name='UserLogin'),
    path('guest_user',views.GuestLogin,name='GuestLogin'),
    path('signup/',views.SignUp,name='SignUp'),
    path('logout',views.Userlogout,name='Userlogout'),
    path('profile/',views.profile,name='profile'),
]
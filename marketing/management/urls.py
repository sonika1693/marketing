from django.urls import path
from . import views
app_name = 'management'

urlpatterns = [
    path('profile/',views.profile,name='profile'),
]
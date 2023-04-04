from django.urls import path
from . import views
app_name = 'content'

urlpatterns = [
    path('',views.Home,name='Home'),
    path('premium/',views.PremiumPackage,name='PremiumPackage'),
    path('package/<int:cat_id>',views.CategoryPackages,name='CategoryPackages'),
    path('details/<int:content_id>',views.Details,name='Details'),
    path('add_comments/',views.AddComents,name='AddComents'),
    path('add_likes/',views.AddLikes,name='AddLikes'),

    path('services/',views.Services,name='Services'),
    path('about/',views.About,name='About'),
    path('shop/',views.Shop,name='Shop'),
    path('contact/',views.Contact,name='Contact'),
    path('testing/',views.Testing,name='Testing'),
]
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
    path('add_cart/<int:content_id>',views.add_cart, name='AddCart'),
    path('delete_cart_item/',views.delete_cart_item, name='delete_cart_item'),
    path('cart/', views.view_cart, name='ViewCart'),
    path('checkout/', views.checkout, name='checkout'),
    path('payment/', views.payment, name='payment'),
    path('success/', views.success, name='success'),
]
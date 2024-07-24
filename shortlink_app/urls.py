from django.urls import path
from . import views

urlpatterns = [
    path('short/', views.short, name='short'),
    path('<str:short_code>/', views.redirect_to_link, name='redirect_to_link'),
    path('check_user/', views.check_user, name='check_user'),
    path('subscribe/', views.subscribe, name='subscribe'),
]

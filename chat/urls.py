from django.urls import path
from django.urls.resolvers import URLPattern
from django.contrib.auth.views import LoginView, LogoutView
from . import views
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from .views import CustomLoginView, UserEditView

urlpatterns = [
    
    path('home/', views.index, name='home'),
    path('home/<str:room_name>/', views.room, name='room'),
    path('', CustomLoginView.as_view(), name='login_url'),
    path('edit_profile', UserEditView.as_view(), name='edit_profile'),
    path('register/',views.registerView,name='register_url'),
    path('logout/',LogoutView.as_view(next_page='login_url'),name='logout' ),
]
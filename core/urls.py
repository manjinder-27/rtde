from django.urls import path
from . import views

urlpatterns = [
    path('',views.homeView,name='home_view'),
    path('login/',views.loginView,name='login_view'),
    path('register/',views.registerView,name='register_view'),
    path('logout/',views.logoutView,name='logout_view'),
]
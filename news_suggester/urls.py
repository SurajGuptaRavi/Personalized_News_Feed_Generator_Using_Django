from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static

from .views import *

urlpatterns = [
    path('',homepage,name="homepage"),
    path('add_to_history',add_to_history,name="add_to_history"),
    path('history',history,name="history"),
    path('about',aboutpage,name="aboutpage"),
    path('login',loginpage,name="loginpage"),
    path('user/login',login_user,name="login_user"),
    path('register',registerpage,name="registerpage"),
    path('user/register',register_user,name="register_user"),
    path('contact',contactpage,name="contactpage"),
    path('user/contact',contact_us,name="contact_us"),
    path('logout',logoutpage,name="logoutpage"),
    path('like_article',like_btn,name="likearticle"),
    path('save_article',save_btn,name="savearticle"),
    path('share_article',share_btn,name="sharearticle"),
    path('saved_article',saved_article,name="savedarticle"),

] 
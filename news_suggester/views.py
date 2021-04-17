from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from django.contrib import messages
import os
from django.conf import settings
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import schedule
import time
import pandas as pd
from .task import *
from django.core.mail import send_mail
import random
import datetime


# Create your views here.

def history(request):
    user_id = request.user.id   
    user_object = User.objects.get(id = int(user_id))

    all_watched_article = reversed(WatchHistory.objects.filter(user = user_object))
    context = {
      'articles':all_watched_article,  
    }
    response = render(request,'history.html',context)
    return HttpResponse(response)
def add_to_history(request):
    
       
    if request.user.is_authenticated and request.method == 'GET':
        article_id = request.GET.get('article_id')
        user_id = request.user.id
        article_object = NewsArticle.objects.get(id = int(article_id))
        user_object = User.objects.get(id = int(user_id))
        
        history_object = WatchHistory()
        history_object.article = article_object
        history_object.user = user_object
        history_object.save()
        return HttpResponse('Added Succesfully in the watch history')

    else:
        return HttpResponse('User is Not Logged In')

def homepage(request):

    
    time_threshold = datetime.datetime.now() - datetime.timedelta(hours=1)

    # all_article = list(NewsArticle.objects.filter(timestamp__lt=time_threshold))
    all_article = list(NewsArticle.objects.all().order_by('-id'))
    print(f"len of all data {len(all_article)}")
    slider_articles = all_article if len(all_article) < 24 else all_article[:24]
    
    politics = list(NewsArticle.objects.filter(timestamp__lt=time_threshold,category='POLITICS').order_by('-timestamp'))
    business = list(NewsArticle.objects.filter(timestamp__lt=time_threshold,category='BUSINESS').order_by('-timestamp'))
    entertainment = list(NewsArticle.objects.filter(timestamp__lt=time_threshold,category='ENTERTAINMENT').order_by('-timestamp'))
    tech = list(NewsArticle.objects.filter(timestamp__lt=time_threshold,category='TECH').order_by('-timestamp'))
    health = list(NewsArticle.objects.filter(timestamp__lt=time_threshold,category='HEALTH').order_by('-timestamp'))
    crime = list(NewsArticle.objects.filter(timestamp__lt=time_threshold,category='CRIME').order_by('-timestamp'))
    sports = list(NewsArticle.objects.filter(timestamp__lt=time_threshold,category='SPORTS').order_by('-timestamp'))

    
    print("length of the crime dataset",len(crime))
    random.shuffle(slider_articles)
    # random.shuffle(all_article)
    # random.shuffle(politics)
    # random.shuffle(business)
    # random.shuffle(entertainment)
    # random.shuffle(tech)
    # random.shuffle(health)
    # random.shuffle(crime)
    # random.shuffle(sports)

    show_only_data = 20

    all_article = all_article if len(all_article) < 20 else all_article[:40]
    politics = politics if len(politics) < show_only_data else politics[:show_only_data]
    business = business if len(business) < show_only_data else business[:show_only_data]
    entertainment = entertainment if len(entertainment) < show_only_data else entertainment[:show_only_data]
    tech = tech if len(tech) < show_only_data else tech[:show_only_data]
    health = health if len(health) < show_only_data else health[:show_only_data]
    crime = crime if len(crime) < show_only_data else crime[:show_only_data]
    sports = sports if len(sports) < show_only_data else sports[:show_only_data]
    
    context = {

        'articles':all_article,
        'slider_articles':slider_articles,
        'politics':politics,
        'business':business,
        'entertainment':entertainment,
        'tech':tech,
        'crime':crime,
        'sports':sports,
        'health':health

        
        }

    if request.user.is_authenticated:
        user_object = User.objects.get(id = int(request.user.id))
        mynews = list(NewsRecommender.objects.filter(user = user_object))
        random.shuffle(mynews)

        context.update({'mynews':mynews})

        response = render(request,'index.html',context)
        return HttpResponse(response)

    else:


    

        response = render(request,'index.html',context)
        return HttpResponse(response)


@login_required(login_url='/login')
def contact_us(request):
    if request.method =='POST' and request.user.is_authenticated:
        user_object = User.objects.get(id = int(request.user.id))
        print(request.POST)
        subject = request.POST.get('subject')
        description = request.POST.get('description')
        email_id = request.POST.get('email')

        contact_object = ContactUs()
        contact_object.user = user_object
        contact_object.subject = subject
        contact_object.email_id = email_id
        contact_object.description = description
        contact_object.save()
        messages.success(request,"Thanks For Contacting Us")
        print("Thanks for contacting us")
        return redirect('homepage')
    else:
        return HttpResponse('Access Denied')
def aboutpage(request):
    response = render(request,'about.html')
    return HttpResponse(response)

def contactpage(request): 
    response = render(request,'contact.html')
    return HttpResponse(response)

def loginpage(request): 
    response = render(request,'login.html')
    return HttpResponse(response)

def login_user(request): 
    if request.method == 'POST':
        user_name = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=user_name,password=password)

        if user is not None:
            login(request,user)
            return redirect('homepage')
        else:
            messages.warning(request,"Incorrect username or password")
            return redirect('loginpage')


    return HttpResponse('Access Denied')

def register_user(request): 
    if request.method =="POST":
        user_name = request.POST['username']
        password = request.POST['password']
        try:
            if User.objects.all().get(username=user_name):
                messages.warning(request,"Username Not Available")
                return redirect('registerpage')
        except:
            new_user = User.objects.create_user(username=user_name,password=password)
            new_user.is_superuser=False
            new_user.is_staff=False
            new_user.save()
            messages.success(request,"Registration Successfull")
            return redirect("loginpage")
    return HttpResponse('Access Denied')

def registerpage(request): 
    response = render(request,'register.html')
    return HttpResponse(response)

@login_required(login_url='/login')
def logoutpage(request):
    if request.method =='GET' and request.user.is_authenticated:
        logout(request)
        messages.success(request,"Logged out successfully")
        print("Logged out successfully")
        return redirect('homepage')
    else:
        return HttpResponse('Access Denied')

def like_btn(request):
    if request.method =='GET' and request.user.is_authenticated:
        article_id = request.GET.get('article_id')
        article_object = NewsArticle.objects.get(id = int(article_id))
        user_object = User.objects.get(id = request.user.id)
        user_action_object = UserActions.objects.filter(article = article_object,user = user_object)

        
        if user_action_object:
            print("User Already created")
            user_action_object = UserActions.objects.get(article = article_object,user = user_object)
            user_action_object.user = user_object
            user_action_object.article = article_object
            user_action_object.liked = True
            print(f"Share value of user is {user_action_object.share}")
            print(f"Saved value of user is {user_action_object.saved}")
            user_action_object.share = user_action_object.share
            user_action_object.saved = user_action_object.saved
            user_action_object.save()
        else:
            print("New Object Created")
            user_action_object = UserActions()
            user_action_object.liked = True
            user_action_object.user = user_object
            user_action_object.article = article_object
            user_action_object.save()

        return HttpResponse("ok")
    else:
        return HttpResponse('Access Denied')


def save_btn(request):
    if request.method =='GET' and request.user.is_authenticated:
        article_id = request.GET.get('article_id')
        article_object = NewsArticle.objects.get(id = int(article_id))
        user_object = User.objects.get(id = request.user.id)
        user_action_object = UserActions.objects.filter(article = article_object,user = user_object)
        if user_action_object:
            user_action_object = UserActions.objects.get(article = article_object,user = user_object)
            user_action_object.user = user_object
            user_action_object.article = article_object
            user_action_object.share = user_action_object.share
            user_action_object.liked= user_action_object.liked
            user_action_object.saved = True
            user_action_object.save()
        else:
            user_action_object = UserActions()
            user_action_object.saved = True
            user_action_object.user = user_object
            user_action_object.article = article_object
            user_action_object.save()

        return HttpResponse("ok")
    else:
        return HttpResponse('Access Denied')

def share_btn(request):
    if request.method =='GET' and request.user.is_authenticated:
        article_id = request.GET.get('article_id')
        article_object = NewsArticle.objects.get(id = int(article_id))
        user_object = User.objects.get(id = request.user.id)
        user_action_object = UserActions.objects.filter(article = article_object,user = user_object)
        if user_action_object:
            user_action_object = UserActions.objects.get(article = article_object,user = user_object)
            user_action_object.user = user_object
            user_action_object.article = article_object
            user_action_object.liked= user_action_object.liked
            user_action_object.saved = user_action_object.saved
            if user_action_object.share:
                user_action_object.share += user_action_object.share
            else:
                user_action_object.share = 1
            user_action_object.save()
        else:
            user_action_object = UserActions()
            user_action_object.share = 1
            user_action_object.user = user_object
            user_action_object.article = article_object
            user_action_object.save()


    
        return HttpResponse("ok")
    else:
        return HttpResponse('Access Denied')


# for showing the saved article to the users
@login_required(login_url='/login')
def saved_article(request):
    user_id = request.user.id   
    user_object = User.objects.get(id = int(user_id))

    all_saved_article = reversed(UserActions.objects.filter(user = user_object,saved = True))
    context = {
      'saved_articles':all_saved_article,  
    }
    response = render(request,'savedarticle.html',context)
    return HttpResponse(response)






 
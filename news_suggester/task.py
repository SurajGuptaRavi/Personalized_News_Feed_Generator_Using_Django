from celery import shared_task
from time import sleep
from django.core.mail import send_mail
from .scrapper import NewsScrapper
import pickle
import pandas as pd
import os
from .models import *

from django.http import HttpResponse
from django.conf import settings
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

# remember run these both commands in 2 diffenerent terminal in your working environment
# celery -A personalized_nfg  beat -l info   // running task with logs  
# celery -A personalized_nfg  worker -l info // ony running a task

# it scrapes the news , predict their category and stores in the database periodically
@shared_task
def predict_category():
    
    Description = 'description'
    Category = 'category'

    if len(NewsArticle.objects.all()) >= 100000:
        df = pd.DataFrame(list(NewsArticle.objects.all().values(Description,Category)))
        category = list(df[Category].unique())
    else:
        #category is based on the pretrained/default model
        category = ['ENTERTAINMENT', 'BUSINESS', 'SPORTS', 'TECH', 'HEALTH', 'POLITICS', 'CRIME']

    category_list = category
    base_path = os.path.join(settings.BASE_DIR,'news_suggester/static/trained_model')
    
    #LOAD MODEL
    loaded_vec = CountVectorizer(vocabulary=pickle.load(open(os.path.join(base_path,"count_vector.pkl"), "rb")))
    loaded_tfidf = pickle.load(open(os.path.join(base_path,"tfidf.pkl"),"rb"))
    loaded_model = pickle.load(open(os.path.join(base_path,"svm.pkl"),"rb"))
    
    for each_news in NewsScrapper().fetch_all_news():
        
        if each_news['description'] != None:
            news = each_news['headlines']
            X_new_counts = loaded_vec.transform([news])
            X_new_tfidf = loaded_tfidf.transform(X_new_counts)
            predicted = loaded_model.predict(X_new_tfidf)
            if NewsArticle.objects.filter(headlines=each_news['headlines']):
                pass
            else:
                article = NewsArticle()
                article.headlines = each_news['headlines']
                article.description = each_news['description']
                article.source_name = each_news['source_name']
                article.author = each_news['author'] if each_news['author']!='' else 'Unknown'
                article.source_link = each_news['source_link']
                article.thumbnail = each_news['thumbnail']
                article.category = category_list[predicted[0]]
                article.save()
    return None

# it fetches all the news article from the databse and convert into the csv files periodically
@shared_task
def get_news_data_csv():
    all_news_data =  NewsArticle.objects.all()
    
    data = []
    for each_news_data in all_news_data:
        each_data_dict = dict()
        each_data_dict['Headlines'] = each_news_data.headlines
        each_data_dict['Description'] = each_news_data.description
        each_data_dict['Category'] = each_news_data.category
        each_data_dict['Author'] = each_news_data.author
        each_data_dict['Source'] = each_news_data.source_name
        each_data_dict['User'] = " "
        each_data_dict['Article_Id'] = each_news_data.id

        data.append(each_data_dict)

    df = pd.DataFrame(data,columns = ['Headlines','Description','Category','Author','Source','User','Article_Id'])
    df.to_csv('all_news.csv')

# it fetches watched history of all user from the databse and convert into the csv files periodically
@shared_task
def get_watched_data():
    watched_data =  WatchHistory.objects.all()
    
    data = []
    for each_watched_data in watched_data:
        each_data_dict = dict()
        each_data_dict['Headlines'] = each_watched_data.article.headlines
        each_data_dict['Description'] = each_watched_data.article.description
        each_data_dict['Category'] = each_watched_data.article.category
        each_data_dict['Author'] = each_watched_data.article.author
        each_data_dict['Source'] = each_watched_data.article.source_name
        each_data_dict['User'] = each_watched_data.user.id
        each_data_dict['Article_Id'] = each_watched_data.article.id

        data.append(each_data_dict)

    df = pd.DataFrame(data,columns = ['Headlines','Description','Category','Author','Source','User','Article_Id'])
    df.to_csv('user_watched_history.csv')
    return None


######################  Content Based Filtering Implemented here  ######################
@shared_task
def fill_suggested_data():
    
    from .content_based_filtering import get_recommended_data
    NewsRecommender.objects.all().delete()
    suggested_data = get_recommended_data()
    try:
        for each_user_id in suggested_data:
            
            try:
                
                user_object = User.objects.get(id = int(each_user_id))
                for article_id in suggested_data[each_user_id][0]['recommended_articles']:
                    article_object = NewsArticle.objects.get(id = int(article_id))

                    recommend_object = NewsRecommender()
                    recommend_object.article = article_object
                    recommend_object.user = user_object
                    recommend_object.save()
                    
            except:
                pass
    except:
        pass

    return None


######################  Model Training Function Scheduled here  ######################
@shared_task     
def model_trainer():
    from .model_trainer import train_the_model
    training_status = train_the_model()
    return training_status



@shared_task
def sleepy(duration):
    sleep(duration)
    return "Task Done"


@shared_task
def send_mail_task():
    # send_mail(
    #     'heading of the mail',
    #     'body of the mail',
    #     'teamdwsuraj@gmail.com',
    #     ['RajeshPurshottamGupta@gmail.com','SurajG@sjcem.edu.in'],
    #     fail_silently = False

    # )

    return None

@shared_task
def send_periodic_mail(receipent):

    # send_mail(
    #     'heading of the mail',
    #     'body of the mail',
    #     'teamdwsuraj@gmail.com',
    #     ['RajeshPurshottamGupta@gmail.com','SurajG@sjcem.edu.in'],
    #     fail_silently = False

    # )
    print(f"Sending Periodic Mail to {receipent}")

    return None



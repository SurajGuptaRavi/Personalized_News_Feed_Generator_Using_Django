from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class NewsArticle(models.Model):
    headlines = models.CharField(max_length = 100,null=False)
    description = models.CharField(max_length = 1000,null=False)
    source_name = models.CharField(max_length = 30,null=True)
    author = models.CharField(max_length = 30,null=True)
    source_link = models.CharField(max_length = 100,null=False)
    category = models.CharField(max_length = 20,null=False)
    thumbnail = models.CharField(max_length = 20,null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.headlines


class WatchHistory(models.Model):
    article = models.ForeignKey(NewsArticle, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.article.headlines



class UserActions(models.Model):
    article = models.ForeignKey(NewsArticle, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    liked = models.BooleanField(null=True)
    share = models.IntegerField(null=True)
    saved = models.BooleanField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.article.headlines
        

class ContactUs(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email_id = models.EmailField(null = False, max_length=254)
    subject = models.CharField(max_length = 1000,null=False)
    description = models.TextField(max_length = 5000)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    


class NewsRecommender(models.Model):
    article = models.ForeignKey(NewsArticle, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.article.headlines



    


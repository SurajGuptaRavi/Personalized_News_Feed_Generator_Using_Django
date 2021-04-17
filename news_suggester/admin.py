from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(NewsArticle)
admin.site.register(WatchHistory)
admin.site.register(NewsRecommender)
admin.site.register(ContactUs)
admin.site.register(UserActions)

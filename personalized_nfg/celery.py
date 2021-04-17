from celery import Celery
import os
from celery.schedules import crontab 


os.environ.setdefault('DJANGO_SETTINGS_MODULE','personalized_nfg.settings')
app = Celery('personalized_nfg')

# Optional configuration, see the application user guide.
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.timezone = 'Asia/Kolkata'

# for sceduling the periodic task
app.conf.beat_schedule = {

    'periodic_mail':{
        'task':'news_suggester.task.send_periodic_mail',
        'schedule':crontab(minute='*/3'), #just for testig purpose
        'args':('Suraj',)
    },
    'Training_SVM_Model':{
        'task':'news_suggester.task.model_trainer',
        'schedule':crontab(0, 0,day_of_month='1-7,15-21'),# first and 3 rd weeks of every month
        
    },
    'news_scrapper':{
        'task':'news_suggester.task.predict_category',
        'schedule':crontab(minute='*/15'), # execures after every 3 hourscrontab(minute=0, hour='*/3')

        # 'args':()
    },
    'all_news_csv':{
        'task':'news_suggester.task.get_news_data_csv',
        'schedule':crontab(minute='*/7'),# execures in every 30 minutes

        # 'args':()
    },
    'watch_history_csv':{
        'task':'news_suggester.task.get_watched_data',
        'schedule':crontab(minute='*/7'), # execures in every 30 minutes
        # 'schedule':crontab(minute=0, hour='*/3'),

        # 'args':()
    },
    'filling_recommended_data':{
        'task':'news_suggester.task.fill_suggested_data',
        'schedule':crontab(minute='*/20'), # execures in every hour

        # 'args':()
    }

}

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
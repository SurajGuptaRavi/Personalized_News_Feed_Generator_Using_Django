import bs4
import requests
class NewsScrapper:
    def __init__(self):
        pass

    # It Scrapes news from newsapi.org website
    def NewsApi(self):
        key="Enter Your API key here"
        url="http://newsapi.org/v2/top-headlines?country=in&apiKey="+key

        res=requests.get(url)
        if str(res.json()['status']).lower() == 'ok':
            news_list = []
            for i in range(1,len(res.json()['articles']) + 1):
                try:
                    each_news = dict()
                    each_news['headlines'] = res.json()['articles'][i-1]['title']
                    each_news['description'] = res.json()['articles'][i-1]['description']
                    each_news['author'] = res.json()['articles'][i-1]['author'] if res.json()['articles'][i-1]['author'] != None else "Unknown"
                    each_news['source_name'] = res.json()['articles'][i-1]['source']['name']
                    each_news['source_link'] = res.json()['articles'][i-1]['url']
                    each_news['thumbnail'] = res.json()['articles'][i-1]['urlToImage']

                    news_list.append(each_news)
                except:
                    pass

        return news_list

    def GNewsApi(self):
        key="Enter your API key here"
        url=f"https://gnews.io/api/v4/search?q=india&token={key}&lang=en"

        res=requests.get(url)
        if True:
            news_list = []
            for i in range(1,len(res.json()['articles']) + 1):
                try:
                    each_news = dict()
                    each_news['headlines'] = res.json()['articles'][i-1]['title']
                    each_news['description'] = res.json()['articles'][i-1]['description']
                    each_news['author'] = "Unknown"
                    each_news['source_name'] = res.json()['articles'][i-1]['source']['name']
                    each_news['source_link'] = res.json()['articles'][i-1]['url']
                    each_news['thumbnail'] = res.json()['articles'][i-1]['image']

                    news_list.append(each_news)
                except:
                    pass

        return news_list

    def fetch_all_news(self):
        all_news = []
        try:
            all_news += self.NewsApi()
        except:
            pass
        try:
            all_news += self.GNewsApi()
        except:
            pass

        
        return all_news

# a  = NewsScrapper()
# print(a.fetch_all_news())

    










    

# Personalized_News_Feed_Generator_Using_Django
  ![](image1.png)
  ![](image2.png)
  
  <ul>
  <li>
            <p>It is a Web Application that provides personalized news & event updates to its users without losing out on time or having to go through irrelevant content.
            </p>
        </li>
        <li>
            <p>Our Website uses Machine Learning Algorithm like Support Vector Machine for classifying the category of the News.
            </p>
        </li>
        <li>
            <p>News articles will be recommended based on clustering of similar articles, predicting their category, content similarity & keyword extraction.
            </p>
        </li>
  <li>
            <p>All information regarding the past clicks, likes, engagement  on this website will be taken into consideration  for future content and predictions.
            </p>
        </li>
        
        
  </ul>
  <b>- Get API key from the following websites</b><br>
  
  <a href="https://newsapi.org/"> Get API from News.org</a> <br>
  <a href="https://gnews.io/"> Get API from GNews.io</a> <br>
  
  <b>- Now go to the news_suggester folder and open scrapper.py file and enter your api key</b><br>
  
<b>- Installations</b><br>
  `pip install -r Requirements.txt`
  
<b>- Open 3 Terminals in your Project Dir where 'manage.py' file is located and paste the following code</b><br>
  `Terminal 1 :- python manage.py runserver`
  
  `Terminal 2 :- celery -A personalized_nfg  beat -l info`
  
  `Terminal 3 :- celery -A personalized_nfg  worker -l info`
  
<a href="https://youtu.be/qd0yf6q7L4E">Demo</a> <br>

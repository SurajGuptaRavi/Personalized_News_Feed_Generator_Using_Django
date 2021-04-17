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
            <p>All information regarding the past clicks, likes, engagement and the amount of time that a user spends on a particular article on this website will be taken into consideration and will be prioritized for future content and predictions.
            </p>
        </li>
  </ul>
  <ol>
    <li><b>Installations<b></li>
          
          pip install -r Requirements.txt
          
  <li><b>Create 3 Terminals and run this 3 commands in the Terminals Respectively<b></li>
        
          python manage.py runserver
          celery -A personalized_nfg  beat -l info
          celery -A personalized_nfg  worker -l info
        
         
  </ol>
   

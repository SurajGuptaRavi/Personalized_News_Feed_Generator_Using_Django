
# importing the required library
import pandas as pd 
from rake_nltk import Rake
import numpy as np 
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer


# loading the csv data files

main_all_news = pd.read_csv('all_news.csv')
main_all_watched_news = pd.read_csv('user_watched_history.csv')


# Considering only suitable coloumns
all_watched_news = main_all_watched_news[['Headlines','Description','Category','Author','Source','User','Article_Id']]
all_news = main_all_news[['Headlines','Description','Category','Author','Source']]

# Shuffling the dataset
all_news = all_news.sample(frac=1).reset_index(drop=True)

# Storing the category,Author and Source into the list
df = all_news

    # Considering only 3 names out of all names of actors and storing in the list
df['Category'] = df['Category'].map(lambda x:x.split(',')[:len(x.split(','))])
    # putting the genre into the list of words
df['Author'] = df['Author'].map(lambda x:x.lower().split(','))
df['Source'] = df['Source'].map(lambda x:x.split(' '))

# lowering the case of category,source and author
for index,row in df.iterrows():
    row['Category'] = [x.lower().replace(' ','') for x in row['Category']]
    row['Source'] = [x.lower().replace(' ','') for x in row['Source']]
    row['Author'] = ''.join(row['Author']).lower()


# Adding new Coloumn in the df "Key_Words"
df['Key_words'] = ''

for index,row in df.iterrows():
    
    # instantiating Rake , by default is uses english stopwards from NLTK
    # and discard all panctuation characters
   
    
    #extracting the words by passing the text
    try:
        Description = row['Description']
        r = Rake()
        r.extract_keywords_from_text(Description)
        key_words_dict_scores = r.get_word_degrees()
        row['Key_words'] = list(key_words_dict_scores.keys())
    except:
        row['Key_words'] = []
    
    #getting the dictionary with key words and their scores
    

    
    #assigning the key words to the new column

    
    

# dropping the plot column
df.drop(columns = ['Description'],inplace = True)

# setting the Headlines coloumns as a index
df.set_index('Headlines',inplace=True)

# Now Combining the rest 4 coloumns into one coloumn named bag_of_words
df['bag_of_words'] = ''
columns = df.columns
for index , row in df.iterrows():
    words = ''
    for col in columns:
        if col != 'Author':
            words = words + ' '.join(row[col]) + ' '
            
        else:
            words = words + row[col] + ' '
            
    row['bag_of_words'] = words
    
df.drop(columns = [col for col in df.columns if col!= 'bag_of_words'],inplace = True)


# Now will ininalize the count vectorizer
# instattiating and generating the count matrix
count = CountVectorizer()
count_matrix = count.fit_transform(df['bag_of_words'])

# creating the series of movie titles so that they r associated to an ordered numerical
# list I will use later to match the indexes
indices = pd.Series(df.index)


# We will measure the cosine similairty matrix
cosine_sim = cosine_similarity(count_matrix,count_matrix)


# recommend function
def recommend_news(headlines,cosine_sim = cosine_sim):
    recommended = []
    #getting the index of the movie that matches the title
    idx = indices[indices == headlines].index[0]
    
    #creating the series with the similarity scores in the descending order
    score_series = pd.Series(cosine_sim[idx]).sort_values(ascending = False)
    
    #getting the index of top 10 similar movies
    top_10_indexes = list(score_series.iloc[1:6].index)
    
    #populating the list with the titles of the best 10 matching movies
    for i in top_10_indexes:
        try:
            recommended.append(list(df.index)[i])
        except:
            pass
        
    return recommended


all_watched_news.drop_duplicates(keep='first',inplace=True)


def get_recommended_data():
    # finding the list of unique users
    
    unique_users = list(all_watched_news['User'].unique())
    suggested_articles = {user:[{'recommended_articles':[],'total_articles':0}] for user in unique_users}
    for each_user in unique_users:
        for index,row in all_watched_news[all_watched_news['User'] == each_user].iterrows():
            articles = recommend_news(row['Headlines'])
            for each_article in articles:
                if each_article not in suggested_articles[each_user][0]['recommended_articles']:
                    try:
                        article_id = int(main_all_news[main_all_news['Headlines'] == each_article]['Article_Id'])
                        suggested_articles[each_user][0]['recommended_articles'].append(article_id)
                        suggested_articles[each_user][0]['total_articles'] = len(suggested_articles[each_user][0]['recommended_articles'])
                    except:
                        pass
        
    return suggested_articles   


# output format of get_recommended_data function is 

"""
{3: [{'recommended_articles': [174,
    182,
    179,
    171,
    178,
    187,
    181,
    170,
    179,
    171],
   'total_articles': 10}],
 1: [{'recommended_articles': [183,
    174,
    175,
    177,
    171,
    174,
    172,
    186,
    180,
    184,
    171,
    175,
    187,
    182,
    179],
   'total_articles': 15}],
 4: [{'recommended_articles': [174, 182, 179, 171, 178], 'total_articles': 5}]}
"""
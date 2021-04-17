
#1 Importing the required Library
import pandas as pd
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn import svm
from sklearn.model_selection import train_test_split
from .models import *
import os
from django.conf import settings


#path of the folder where all files will be stored
base_path = os.path.join(settings.BASE_DIR,'news_suggester/static/trained_model')


#2 Loading the Dataset from the database
Description = 'description'
Category = 'category'
data_size = 100000
def train_the_model():
	df = pd.DataFrame(list(NewsArticle.objects.all().values(Description,Category)))

	if len(df[Description]) >= data_size and len(df[Description]) <= 500000:
		#3 Getting the list of all categories
		categories = list(df[Category].unique())


		#4 Converting the Category coloumn into numerical coloumn
		df[Category] = df[Category].map(lambda x:categories.index(x))


		#5 Creating the vector count
		count_vect = CountVectorizer()
		X_train_counts = count_vect.fit_transform(df[Description])
		pickle.dump(count_vect.vocabulary_, open(os.path.join(base_path,"count_vector.pkl"),"wb"))


		#6 Creating the TFUD 
		tfidf_transformer = TfidfTransformer()
		X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
		pickle.dump(tfidf_transformer, open(os.path.join(base_path,"tfidf.pkl"),"wb"))


		#7 Training the model
		clf_svm = svm.LinearSVC()
		X_train, X_test, y_train, y_test = train_test_split(X_train_tfidf, df[Category], test_size=0.20, random_state=42)
		clf_svm.fit(X_train_tfidf, df[Category])
		pickle.dump(clf_svm, open(os.path.join(base_path,"svm.pkl"), "wb"))
		
		return "Training Successfully"
	else:
		return "Very Less Data to Train"
	
	
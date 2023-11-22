# %%
import pandas as pd
import numpy as np
import re
import nltk

# %%
df=pd.read_csv("IMDB_OMDB_Kaggle_TestSet_OMDB_Detailed.csv")

# %%
df['clean_plot']=df['Plot'].str.lower()
df['clean_plot']=df['clean_plot'].apply(lambda x: re.sub('[^a-zA-Z]',' ',x))
df['clean_plot']=df['clean_plot'].apply(lambda x: re.sub('\s+',' ',x))

# %%
df['clean_plot']=df["clean_plot"].apply(lambda x: nltk.word_tokenize(x))

# %%
stop_word=nltk.corpus.stopwords.words('english')
plot=[]
for sentence in df['clean_plot']:
    temp=[]
    for word in sentence:
        if word not in stop_word and len(word)>=3:
            temp.append(word)
    plot.append(temp)


# %%
df['clean_plot']=plot

# %%
plot

# %%
df['Genre']=df['Genre'].apply(lambda x: x.split(','))
df['Actors']=df['Actors'].apply(lambda x: x.split(','))
df['Director']=df['Director'].apply(lambda x: x.split(','))

# %%
def clean(sentence):
    temp=[]
    for word in sentence:
        temp.append(word.lower().replace(' ',' '))
    return temp

# %%
df['Genre']=[clean(x)for x in df['Genre']]


# %%
df['Actors']=[clean(x) for x in df['Actors']]

# %%
df['Director']=[clean(x) for x in df['Director']]

# %%
df.head()

# %%
df['Actors'][0]

# %%
columns=['clean_plot','Genre','Actors','Director']
l=[]
for i in range(len(df)):
    words=''
    for col in columns:
        words+=' '.join(df[col][i])+' '
    l.append(words)
l

# %%
df['clean_input']=l
df=df[['Title','clean_input']]

# %%
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
tfidf=TfidfVectorizer()
features=tfidf.fit_transform(df['clean_input'])

# %%
from sklearn.metrics.pairwise import cosine_similarity
cosine_sim=cosine_similarity(features,features)
print(cosine_sim)

# %%
index=pd.Series(df['Title'])
index.head()

# %%
def recommend_movies(title):
    movies=[]
    idx=index[index==title].index[0]
    score=pd.Series(cosine_sim[idx]).sort_values(ascending=False)
    top10=list(score.iloc[1:11].index)

    for i in top10:
        movies.append(df['Title'][i])
    return movies

# %%
df['Title']

# %%
recommend_movies()

# %%
while True:
    a=input(print("ENTER THE MOVIE NAME:"))
    recommend_movies(a)





from cmath import cos
from django.shortcuts import render
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

#--------------------------------Getting movie similarity matrix using cosine similarity from sklearn---------------------------------- 

df = pd.read_csv(r"movies.csv")
features = ['keywords', 'cast', 'genres', 'director']
#replace any rows having NaN values with a space, so that it does not generate an error while running 
for feature in features:
    df[feature] = df[feature].fillna('')
#adding a new column, combined_features to our dataframe and apply the above function to each row (axis = 1).
def combined_features(row):
    return row['keywords']+" "+row['cast']+" "+row['genres']+" "+row['director']
df["combined_features"] = df.apply(combined_features, axis =1)
#CountVectorizer to convert collection of text documents to vector of term or token counts
cv = CountVectorizer()
count_matrix = cv.fit_transform(df["combined_features"])
count_matrix.toarray()
cosine_sim = cosine_similarity(count_matrix)
# --------------------------------------------------------------------------------------------------------------------------------------------

#-----------------------------views starts here------------------------
def index(request):
    movie_user_likes = "Harry Potter and the Half-Blood Prince"
    def get_index_from_title(title):
        return df[df.title == title]["index"].values[0]
    movie_index = get_index_from_title(movie_user_likes)
    similar_movies = list(enumerate(cosine_sim[movie_index]))
    def get_title_from_index(index):
        return df[df.index == index]["title"].values[0]
    i=0
    sorted_similar_movies = sorted(similar_movies, key=lambda x:x[1], reverse=True)
    for movie in sorted_similar_movies:
        print(get_title_from_index(movie[0]))
        i=i+1
        if i>20:
            break
    return render(request,'recommend/index.html')
def displaymovie(request):
    return render(request,'recommend/displaymovie.html')

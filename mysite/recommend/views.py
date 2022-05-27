from cmath import cos
from operator import itemgetter
from django.shortcuts import render
# import pandas as pd
from . import models
# from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.metrics.pairwise import cosine_similarity

#--------------------------------Getting movie similarity matrix using cosine similarity from sklearn---------------------------------- 

# df = pd.read_csv(r"movies.csv")
# features = ['keywords', 'cast', 'genres', 'director']
# #replace any rows having NaN values with a space, so that it does not generate an error while running 
# for feature in features:
#     df[feature] = df[feature].fillna('')
# #adding a new column, combined_features to our dataframe and apply the above function to each row (axis = 1).
# def combined_features(row):
#     return row['keywords']+" "+row['cast']+" "+row['genres']+" "+row['director']
# df["combined_features"] = df.apply(combined_features, axis =1)
# #CountVectorizer to convert collection of text documents to vector of term or token counts
# cv = CountVectorizer()
# count_matrix = cv.fit_transform(df["combined_features"])
# count_matrix.toarray()
# cosine_sim = cosine_similarity(count_matrix)
# # --------------------------------------------------------------------------------------------------------------------------------------------

# #getting movie sorted based on average voting and then popularity, to get recommendation if user opened app for first time
# ind=0
# movie_rating=[]
# for (i,j) in zip(df['vote_average'],df['popularity']):
#     movie_rating.append((ind,i,j))
#     ind=ind+1
# movie_sorted=sorted(movie_rating,key=itemgetter(1,2),reverse=True)
# movie_sorted_on_rating=[]
# for i in movie_sorted:
#     movie_sorted_on_rating.append(i[0])
#-----------------------------views starts here------------------------
def index(request):
    # likedmovies=models.Liked_movies.objects.all()
    # watchedmovies=models.Watched_movies.objects.all()
    # searchedmovies=models.Searched_movies.objects.all()
    disp=[]
    # if(len(likedmovies)==0 and len(watchedmovies)==0 and len(searchedmovies)==0 ):
    #     for i in range(0,15):
    #         disp.append(movie_sorted_on_rating[i])
    # else:

    #     movie_user_likes = "Harry Potter and the Half-Blood Prince"
    #     def get_index_from_title(title):
    #         return df[df.title == title]["index"].values[0]
    #     movie_index = get_index_from_title(movie_user_likes)
    #     similar_movies = list(enumerate(cosine_sim[movie_index]))
    #     def get_title_from_index(index):
    #         return df[df.index == index]["title"].values[0]
    #     i=0
    #     sorted_similar_movies = sorted(similar_movies, key=lambda x:x[1], reverse=True)
    #     for movie in sorted_similar_movies:
    #         # print(get_title_from_index(movie[0]))
    #         i=i+1
    #         if i>20:
    #             break
    return render(request,'recommend/index.html',context={'moviedisp':disp})
def displaymovie(request):
    return render(request,'recommend/displaymovie.html')
def index2(request):
    return render(request,'recommend/index2.html')

#list for liked movies - movie id - bool liked - this needs to be stored in db as a table?
#list of watched movies - movie id - bool watched
# list of searched movies, i.e., whichever movie came in the first - movie id - bool watched
#rating we already know ryt...so movies sorted on basis of ratings, this we can make as global


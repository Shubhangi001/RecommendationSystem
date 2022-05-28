from cmath import cos
from operator import itemgetter
from django.http import HttpResponseRedirect
from django.shortcuts import render
from numpy import equal
import pandas as pd
from . import models
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
# # --------------------------------------------------------------------------------------------------------------------------------------------

# #getting movie sorted based on average voting and then popularity, to get recommendation if user opened app for first time
ind=0
movie_rating=[]
for (i,j) in zip(df['vote_average'],df['popularity']):
    movie_rating.append((ind,i,j))
    ind=ind+1
movie_sorted=sorted(movie_rating,key=itemgetter(1,2),reverse=True)
movie_sorted_on_rating=[]
for i in movie_sorted:
    movie_sorted_on_rating.append(i[0])
#-----------------------------views starts here------------------------
def index(request):
    watchedmovies=models.Watched_movies.objects.all()
    searchedmovies=models.Searched_movies.objects.all()
    savedmovies=models.Saved_movies.objects.all()
    likedmovies=models.Liked_movies.objects.all()
    disp=[]
    def get_title_from_index(index):
        return df[df.index == index]["title"].values[0]
    if(len(likedmovies)==0 and len(watchedmovies)==0 and len(searchedmovies)==0 and len(savedmovies)==0):
        for i in range(0,50):
            disp.append(get_title_from_index(movie_sorted_on_rating[i]))
    else:
        liked=[]
        watched=[]
        towatch=[]
        searched=[]
        def get_similar_movies(l):
            res=[]
            for x in l:
                movie_index = x.movie_id_id
                similar_movies = list(enumerate(cosine_sim[movie_index]))
                i=0
                sorted_similar_movies = sorted(similar_movies, key=lambda x:x[1], reverse=True)
                temp=[]
                for movie in sorted_similar_movies:
                    temp.append(movie[0])
                    i=i+1
                    if i>20:
                        break
                if(len(temp)<15):
                    for i in range(len(temp),15):
                        temp.append(0)
                res.append(temp)
            return res
        liked=get_similar_movies(likedmovies)
        watched=get_similar_movies(watchedmovies)
        towatch=get_similar_movies(savedmovies)
        searched=get_similar_movies(searchedmovies)
        for movie in range(0,15):
            dicti={}
            for movielist in liked:
                if movielist[movie] != -1:
                    if movielist[movie] in dicti:
                        dicti[movielist[movie]]=dicti[movielist[movie]]+0.5
                    else:
                        dicti[movielist[movie]]=0
            for movielist in towatch:
                if movielist[movie] != -1:
                    if movielist[movie] in dicti:
                        dicti[movielist[movie]]=dicti[movielist[movie]]+0.3
                    else:
                        dicti[movielist[movie]]=0
            for movielist in watched:
                if movielist[movie] != -1:
                    if movielist[movie] in dicti:
                        dicti[movielist[movie]]=dicti[movielist[movie]]+0.3
                    else:
                        dicti[movielist[movie]]=0
            for movielist in searched:
                if movielist[movie] != -1:
                    if movielist[movie] in dicti:
                        dicti[movielist[movie]]=dicti[movielist[movie]]+0.3
                    else:
                        dicti[movielist[movie]]=0
            maxrecommovie = max(dicti, key= lambda x: dicti[x])
            disp.append(maxrecommovie)
    return render(request,'recommend/index.html',context={'moviedisp':disp,'likedmovies':likedmovies})
def displaymovie(request):
    return render(request,'recommend/displaymovie.html')
def likedlist(request):
    likedmovies=models.Liked_movies.objects.all()
        
    if(request.method =="POST"):
        movid=request.POST.get('likedid')
        if movid not in likedmovies:
            item=models.Liked_movies.objects.get_or_create(movie_id_id=int(movid))
        # return HttpResponseRedirect('index')
    return HttpResponseRedirect('index')
def watchlist(request):
    savedmovies=models.Saved_movies.objects.all()
    if(request.method =="POST"):
        movid=request.POST.get('watchid')
        if movid not in savedmovies:
            item=models.Saved_movies.objects.get_or_create(movie_id_id=int(movid))
        return HttpResponseRedirect('index')
    return HttpResponseRedirect('index')
def watchedlist(request):
    watchedmovies=models.Watched_movies.objects.all()
    if(request.method =="POST"):
        movid=request.POST.get('watchedid')
        if movid not in watchedmovies:
            item=models.Watched_movies.objects.get_or_create(movie_id_id=int(movid))
        return HttpResponseRedirect('index')
    return HttpResponseRedirect('index')
def savedhistory(request):
    watchedmovies=models.Watched_movies.objects.all()
    likedmovies=models.Liked_movies.objects.all()
    savedmovies=models.Saved_movies.objects.all()
    return render(request,'recommend/history.html',context={'disp':savedmovies,'likedmovies':likedmovies,'watchedmovies':watchedmovies,'savedmovies':savedmovies})
def likedhistory(request):
    likedmovies=models.Liked_movies.objects.all()
    watchedmovies=models.Watched_movies.objects.all()
    savedmovies=models.Saved_movies.objects.all()
    return render(request,'recommend/history.html',context={'disp':likedmovies,'likedmovies':likedmovies,'watchedmovies':watchedmovies,'savedmovies':savedmovies})
def watchedhistory(request):
    likedmovies=models.Liked_movies.objects.all()
    savedmovies=models.Saved_movies.objects.all()
    watchedmovies=models.Watched_movies.objects.all()
    return render(request,'recommend/history.html',context={'disp':watchedmovies,'likedmovies':likedmovies,'watchedmovies':watchedmovies,'savedmovies':savedmovies})
def trending(request):
    likedmovies=models.Liked_movies.objects.values_list('movie_id_id')
    savedmovies=models.Saved_movies.objects.all()
    watchedmovies=models.Watched_movies.objects.all()
    disp=[]
    for i in range(0,30):
            disp.append(movie_sorted_on_rating[i])
    return render(request,'recommend/history.html',context={'disp':disp,'likedmovies':likedmovies,'watchedmovies':watchedmovies,'savedmovies':savedmovies})


#list for liked movies - movie id - bool liked - this needs to be stored in db as a table?
#list of watched movies - movie id - bool watched
# list of searched movies, i.e., whichever movie came in the first - movie id - bool watched
#rating we already know ryt...so movies sorted on basis of ratings, this we can make as global


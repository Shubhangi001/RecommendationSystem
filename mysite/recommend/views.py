from operator import itemgetter, mod
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.db.models import Q
import pandas as pd
import numpy as np
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
    m=models.Movie.objects.get(id=i[0])
    movie_sorted_on_rating.append(m)
#-------------------------------------views starts here------------------------\
def index(request):
    def get_similar_movies(l):   # get 15 most similar movies for the given movie history
                res=[]
                for x in l:               #iteratin in watched/saved/liked/searched list
                    movie_index = x.movie_id_id
                    similar_movies = list(enumerate(cosine_sim[movie_index]))         #get the list of similar movie for the current movie
                    i=0
                    sorted_similar_movies = sorted(similar_movies, key=lambda x:x[1], reverse=True)  #sorting it in descending order to get most similar
                    temp=[]
                    for movie in sorted_similar_movies: #getting 15 most similar movie for the given movie   
                        temp.append(movie[0])  
                        i=i+1
                        if i>30:
                            break
                    if(len(temp)<30):
                        for i in range(len(temp),30):
                            temp.append(0)
                    res.append(temp)                #list of list of similar movies for each history
                return res
    watchedmovies=models.Watched_movies.objects.all()
    searchedmovies=models.Searched_movies.objects.all()
    savedmovies=models.Saved_movies.objects.all()
    likedmovies=models.Liked_movies.objects.all()
    disp=[]
    def get_title_from_index(index):
        return df[df.index == index]["title"].values[0]
    #if user hasn't given any input yet
    if(len(likedmovies)==0 and len(watchedmovies)==0 and len(searchedmovies)==0 and len(savedmovies)==0):
        for i in range(0,50):
            disp.append(movie_sorted_on_rating[i])
    else:             #recommendation based on like,watch,search,save history
        liked=[]
        watched=[]
        towatch=[]
        searched=[]
        
        liked=get_similar_movies(likedmovies)
        watched=get_similar_movies(watchedmovies)
        towatch=get_similar_movies(savedmovies)
        searched=get_similar_movies(searchedmovies)
        for i in range(0,30):               #for each index find the movie which is most common in all giving 45% weightage
                                                #to liked movies, 35% to saved movies, 15% to watched and 5% to searched
            dicti={}
            for movielist in liked:
                if movielist[i] != -1:
                    if movielist[i] in dicti:
                        dicti[movielist[i]]=dicti[movielist[i]]+0.945
                    else:
                        dicti[movielist[i]]=0
            for movielist in towatch:
                if movielist[i] != -1:
                    if movielist[i] in dicti:
                        dicti[movielist[i]]=dicti[movielist[i]]+0.935
                    else:
                        dicti[movielist[i]]=0
            for movielist in watched:
                if movielist[i] != -1:
                    if movielist[i] in dicti:
                        dicti[movielist[i]]=dicti[movielist[i]]+0.915
                    else:
                        dicti[movielist[i]]=0
            for movielist in searched:
                if movielist[i] != -1:
                    if movielist[i] in dicti:
                        dicti[movielist[i]]=dicti[movielist[i]]+0.905
                    else:
                        dicti[movielist[i]]=0
            p = max(dicti, key= lambda x: dicti[x]) 
            maxrecommovie=models.Movie.objects.get(id=p)
            disp.append(maxrecommovie)

    disp=list(dict.fromkeys(disp))
    return render(request,'recommend/index.html',context={'moviedisp':disp,'likedmovies':likedmovies})
def displaymovie(request):
    return render(request,'recommend/displaymovie.html')
def likedlist(request):
    likedmovies=models.Liked_movies.objects.all()
        
    if(request.method =="POST"):
        movid=request.POST.get('likedid')
        models.Liked_movies.objects.get_or_create(movie_id_id=int(movid))
    return HttpResponseRedirect('index')
def watchlist(request):
    savedmovies=models.Saved_movies.objects.all()
    if(request.method =="POST"):
        movid=request.POST.get('watchid')
        models.Saved_movies.objects.get_or_create(movie_id_id=int(movid))
        return HttpResponseRedirect('index')
    return HttpResponseRedirect('index')
def watchedlist(request):
    watchedmovies=models.Watched_movies.objects.all()
    if(request.method =="POST"):
        movid=request.POST.get('watchedid')
        models.Watched_movies.objects.get_or_create(movie_id_id=int(movid))
        return HttpResponseRedirect('index')
    return HttpResponseRedirect('index')
def savedhistory(request):
    watchedmovies=models.Watched_movies.objects.all()
    likedmovies=models.Liked_movies.objects.all()
    savedmovies=models.Saved_movies.objects.all()
    disp=[]
    for i in savedmovies:
        movie=models.Movie.objects.get(id=i.movie_id_id)
        disp.append(movie)
    return render(request,'recommend/history.html',context={'disp':disp,'likedmovies':likedmovies,'watchedmovies':watchedmovies,'savedmovies':savedmovies})
def likedhistory(request):
    likedmovies=models.Liked_movies.objects.all()
    watchedmovies=models.Watched_movies.objects.all()
    savedmovies=models.Saved_movies.objects.all()
    disp=[]
    for i in likedmovies:
        movie=models.Movie.objects.get(id=i.movie_id_id)
        disp.append(movie)
    return render(request,'recommend/history.html',context={'disp':disp,'likedmovies':likedmovies,'watchedmovies':watchedmovies,'savedmovies':savedmovies})
def watchedhistory(request):
    likedmovies=models.Liked_movies.objects.all()
    savedmovies=models.Saved_movies.objects.all()
    watchedmovies=models.Watched_movies.objects.all()
    disp=[]
    for i in watchedmovies:
        movie=models.Movie.objects.get(id=i.movie_id_id)
        disp.append(movie)
    return render(request,'recommend/history.html',context={'disp':disp,'likedmovies':likedmovies,'watchedmovies':watchedmovies,'savedmovies':savedmovies})
def trending(request):
    likedmovies=models.Liked_movies.objects.values_list('movie_id_id')
    savedmovies=models.Saved_movies.objects.all()
    watchedmovies=models.Watched_movies.objects.all()
    disp=[]
    for i in range(29,0,-1):
            disp.append(movie_sorted_on_rating[i])
    return render(request,'recommend/history.html',context={'disp':disp,'likedmovies':likedmovies,'watchedmovies':watchedmovies,'savedmovies':savedmovies})
def search_movies(request):
    if(request.method=="POST"):
        searched=request.POST.get('searched')
        c1=Q(original_title__contains=searched) 
        c2=Q(cast__contains=searched) 
        c3= Q(genres__contains=searched) 
        c4= Q(keywords__contains=searched)
        c5= Q(spoken_language__contains=searched)
        allmovies=models.Movie.objects.filter(c1|c2|c3|c4|c5)
        movies=allmovies[0:20]
        if(len(allmovies)!=0):
            models.Searched_movies.objects.get_or_create(movie_id_id=movies[0].id)   #the first search query result is stored in searched movies
        else:
            return HttpResponseRedirect('index')
        return render(request,'recommend/search.html',{'searched':searched,'movies':movies})
    else:
        return HttpResponseRedirect('index')

#list for liked movies - movie id -  - this needs to be stored in db as a table
#list of watched movies - movie id 
# list of searched movies, i.e., whichever movie came in the first - movie id 
#rating we already know ryt...so movies sorted on basis of ratings, this we can make as global


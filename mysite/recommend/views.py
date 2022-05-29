from operator import itemgetter, mod
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.db.models import Q
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
#-------------------------------------views starts here------------------------
def index(request):
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
            disp.append(get_title_from_index(movie_sorted_on_rating[i]))
    else:             #recommendation based on like,watch,search,save history
        liked=[]
        watched=[]
        towatch=[]
        searched=[]
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
                    if i>15:
                        break
                if(len(temp)<15):
                    for i in range(len(temp),15):
                        temp.append(0)
                res.append(temp)                #list of list of similar movies for each history
            return res
        liked=get_similar_movies(likedmovies)
        watched=get_similar_movies(watchedmovies)
        towatch=get_similar_movies(savedmovies)
        searched=get_similar_movies(searchedmovies)
        for i in range(0,15):               #for each index find the movie which is most common in all giving 50% weightage
                                                #to liked movies, 30% to saved movies, 15% to watched and 5% to searched
            dicti={}
            for movielist in liked:
                if movielist[i] != -1:
                    if movielist[i] in dicti:
                        dicti[movielist[i]]=dicti[movielist[i]]+0.5
                    else:
                        dicti[movielist[i]]=0
            for movielist in towatch:
                if movielist[i] != -1:
                    if movielist[i] in dicti:
                        dicti[movielist[i]]=dicti[movielist[i]]+0.3
                    else:
                        dicti[movielist[i]]=0
            for movielist in watched:
                if movielist[i] != -1:
                    if movielist[i] in dicti:
                        dicti[movielist[i]]=dicti[movielist[i]]+0.15
                    else:
                        dicti[movielist[i]]=0
            for movielist in searched:
                if movielist[i] != -1:
                    if movielist[i] in dicti:
                        dicti[movielist[i]]=dicti[movielist[i]]+0.05
                    else:
                        dicti[movielist[i]]=0
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
def search_movies(request):
    if(request.method=="POST"):
        searched=request.POST.get('searched')
        movies=models.Movie.objects.filter(Q(original_title__contains=searched) or Q(cast__contains=searched) or Q(genres__contains=searched) or Q(keywords__contains=searched) or Q(spoken_language__contains=searched))
        return render(request,'recommend/search.html',{'searched':searched,'movies':movies})
    else:
        return HttpResponseRedirect('index')

#list for liked movies - movie id -  - this needs to be stored in db as a table
#list of watched movies - movie id 
# list of searched movies, i.e., whichever movie came in the first - movie id 
#rating we already know ryt...so movies sorted on basis of ratings, this we can make as global


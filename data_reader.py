import pandas as pd
from pprint import pprint
import actions_collections as db_actions 
import math

def generateMovieDocs():
    movies = {}
    df_movies = pd.read_csv('./data/movies/MovieInfoStash_FINAL.csv')

    # Load basic info
    for index, row in df_movies.iterrows():
        movieId = str(row[0])
        movie = {
            '_id': movieId,
            'movieId': movieId,
            'title': row[1],
        }
        if isinstance(row[2], str):
            movie['year'] = row[2]
        movies[movieId] = movie
    
    # Load countries
    df_countries = pd.read_csv('./data/movies/Movie_country.csv')
    for index, row in df_countries.iterrows():
        movieId = str(row[0])
        movie = movies[movieId]
        movie['country'] = row[1]           
        movies[movieId] = movie

    # Load actors
    df_actors = pd.read_csv('./data/movies/MovieActorsStash_FINAL.csv')
    for index, row in df_actors.iterrows():
        movieId = str(row[0])
        movie = movies[movieId]
        if 'actors' in movie:
            movie['actors'].append(row[1])
        else:
            movie['actors'] = [row[1]]    
        movies[movieId] = movie
    
    # Load director
    df_director = pd.read_csv('./data/movies/MovieDirector_FINAL.csv')
    for index, row in df_director.iterrows():
        movieId = str(row[0])
        movie = movies[movieId]
        movie['director'] = row[1]           
        movies[movieId] = movie

    # Load genres
    df_actors = pd.read_csv('./data/movies/movie_genre.csv')
    for index, row in df_actors.iterrows():
        movieId = str(row[0])
        movie = movies[movieId]
        if 'genres' in movie:
            movie['genres'].append(row[1])
        else:
            movie['genres'] = [row[1]]    
        movies[movieId] = movie
    
    return movies

def generateReviewsDocs():
    CF_train = pd.read_pickle("./data/ratings/train.pkl")
    CF_test = pd.read_pickle("./data/ratings/test.pkl")
    CF_validation = pd.read_pickle("./data/ratings/validation.pkl")

    CF_general = pd.concat([CF_test, CF_train, CF_validation])
    # print(CF_general)
    
    users = {}
    movie_reviews = {}
    count = 0
    for index, row in CF_general.iterrows():
        userId = str(row[0])
        movieId = str(row[1])
        user = None
        if userId in users:
            user = users[userId]
        else:
            user = {
                '_id': userId,
                'userId': userId,
                'genre_dist': {},
                'reviews': {},
                'window': 0,
                'reviews_list': [],
                'disliked': [],
                'liked': [],
            }
        
        movie = None
        if movieId in movie_reviews:
            movie = movie_reviews[movieId]
        else:
            movie = {
                'cant_reviews': 0,
                'reviews': {},
                'reviews_list': [],
            }

        
        user = db_actions.update_reviews_user(movieId, row[2], user)
        user = db_actions.update_genre_dist(row[6].split('|'), user)
        users[userId] = user
        
        movie = db_actions.update_reviews_movie(userId, row[2], movie)
        movie['cant_reviews'] = movie['cant_reviews']+1
        movie_reviews[movieId] = movie

        count += 1
        if count%10000 == 0:
            print(f'At {count}')
    return users, movie_reviews
        
def generateUserAndMovieDocs():
    movies = generateMovieDocs()
    users, movie_reviews = generateReviewsDocs()
    count_noreviews = 0
    for movieId in movies:
        movie = movies[movieId]
        if movieId in movie_reviews:
            movie['reviews'] = movie_reviews[movieId]['reviews']
            movie['reviews_list'] = movie_reviews[movieId]['reviews_list']
            movie['cant_reviews'] = movie_reviews[movieId]['cant_reviews']
        else:
            movie['reviews'] = {}
            movie['reviews_list'] = []
            movie['cant_reviews'] = 0
            count_noreviews += 1
            print(f'STFU mate, movie {movie} not in reviews bro!')
        movies[movieId] = movie
    print(f'Total no reviews: {count_noreviews}')
    return users, movies
        

            


if __name__ == "__main__":
    users, movies = generateUserAndMovieDocs()
    pprint(users[84337])
    pprint(movies[2])

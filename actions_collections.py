import copy

def update_genre_dist(genres, user):
    p_user = copy.copy(user)
    genre_dist = p_user['genre_dist']
    for genre in genres:
        if genre in genre_dist:
            genre_dist[genre]['count'] = genre_dist[genre]['count'] + 1
        else: 
            genre_data = { 'count': 1 }
            genre_dist[genre] = genre_data
    p_user['genre_dist'] = genre_dist
    return p_user

def update_reviews_user(movieId, rating, user):
    p_user = copy.copy(user)
    p_user['reviews'][movieId] = rating
    p_user['reviews_list'].append((movieId, rating))
    return p_user

def update_reviews_movie(userId, rating, movie):
    p_movie = copy.copy(movie)
    p_movie['reviews'][userId] = rating
    p_movie['reviews_list'].append((userId, rating))
    return p_movie
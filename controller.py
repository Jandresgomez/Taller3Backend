import re
import random
import actions_collections as actions
import recommender.recommendations_generator as recommender


def get_user_by_id(db, userId):
    if not userId is None:
        res = db.find_one({"_id": userId})
        if not res is None:
            return res
        return False
    return False


def create_user_with_id(db, userId):
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
    db.insert_one(user)
    return user


def get_history(db_movies, db_users, userId):
    user_data = get_user_by_id(db_users, userId)
    if not user_data:
        return []
    history_ids = user_data['liked']
    res = db_movies.find({"_id": {"$in": history_ids}}).limit(100)
    if not res is None:
        res = list(res)
        return res
    else:
        return []


def get_recommedations(db_movies, db_users, db_neo, userId):
    user_data = get_user_by_id(db_users, userId)
    if not user_data:
        return []

    liked_ids = user_data['liked']
    disliked_ids = user_data['disliked']
    window = user_data['window']
    random.seed(window)

    liked_ids = random.sample(liked_ids, min(3, len(liked_ids)))
    recom_ids = recommender.filtered_recommendations(
        db_neo, liked_ids, disliked_ids)
    recom_ids = random.sample(recom_ids, min(10, len(recom_ids)))

    res = db_movies.find({"_id": {"$in": recom_ids}})
    if not res is None:
        res = list(res)
        return res
    else:
        return []


def update_recom_window(db_users, userId):
    db_users.update({'_id': userId}, {'$inc': {'window': 1}})


def find_movies_with_partial(db, partial_name, page, page_length):
    regx = re.compile(f'{partial_name}.*', re.IGNORECASE)
    res = db.find({"title": {'$regex': regx}}).skip(
        page*page_length).limit(page_length)
    if not res is None:
        res = list(res)
        return res
    else:
        return []


def find_movie_by_id(db, movieId):
    if not movieId is None:
        res = db.find_one({"_id": movieId})
        if not res is None:
            return res
        return False
    return False


def like_movie(db_users, db_movies, userId, movieId):
    user_data = get_user_by_id(db_users, userId)
    if not user_data:
        return False
    movie_data = find_movie_by_id(db_movies, movieId)
    if not movie_data:
        return False

    new_disliked = list(filter(lambda a: a != movieId, user_data['disliked']))
    new_liked = list(filter(lambda a: a != movieId, user_data['liked']))
    new_liked.append(movieId)
    genre_dist = actions.update_genre_dist(movie_data['genres'], user_data)

    db_users.update({'_id': userId}, {
        '$push': {
            'reviews_list': (movieId, 5.0),
        },
        '$set': {
            'genre_dist': genre_dist,
            'disliked': new_disliked,
            'liked': new_liked,
            f'reviews.{movieId}': 5.0,
        }
    })
    db_movies.update({'_id': movieId}, {
        '$push': {
            'reviews_list': (movieId, 5.0),
        },
        '$set': {
            f'reviews.{userId}': 5.0,
        }
    })
    return True


def dislike_movie(db_users, userId, movieId):
    user_data = get_user_by_id(db_users, userId)
    if not user_data:
        return False

    new_liked = list(filter(lambda a: a != movieId, user_data['liked']))
    new_disliked = list(filter(lambda a: a != movieId, user_data['disliked']))
    new_disliked.append(movieId)

    db_users.update({'_id': userId}, {
        '$set': {
            'liked': new_liked,
            'disliked': new_disliked,
        }
    })


def find_top_movies(db_movie, size):
    res = db_movie.find().sort({"cant_reviews": -1}).limit(size)
    if not res is None:
        res = list(res)
        return res

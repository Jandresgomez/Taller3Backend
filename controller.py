import re 

def get_user_by_id(db, userId):
    if not userId is None:
        res = db.find_one({"_id": userId })
        if not res is None:
            return res
        return False
    return False

def get_history(db_movies, db_users, userId):
    user_data = get_user_by_id(db_users, userId)
    if not user_data:
        return []
    review_ids = list(user_data['reviews'].keys())
    res = db_movies.find({"_id" : {"$in" : review_ids}}).limit(100)
    if not res is None:
        res = list(res)
        return res
    else:
        return []
    

def find_movies_with_partial(db, partial_name, page, page_length):
    regx = re.compile(f'{partial_name}.*', re.IGNORECASE)
    res = db.find({"title": {'$regex': regx}}).skip(page*page_length).limit(page_length)
    if not res is None:
        res = list(res)
        return res
    else: 
        return []

def find_movie_by_id(db, movieId):
    if not movieId is None:
        res = db.find_one({"_id": movieId })
        if not res is None:
            return res
        return False
    return False
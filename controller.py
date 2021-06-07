import re 

def getUserByUserId(db, userId):
    if not userId is None:
        res = db.find_one({"_id": userId })
        print(res)
        if not res is None:
            return res
        return False
    return False

def find_movies_with_partial(db, partial_name, page, page_length):
    regx = re.compile(f'{partial_name}.*', re.IGNORECASE)
    res = db.find({"title": {'$regex': regx}}).skip(page*page_length).limit(page_length)
    if not res is None:
        res = list(res)
        return res
    else: 
        return []
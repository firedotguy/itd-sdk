from itd.request import fetch

def search(token: str, query: str, user_limit: int = 5, hashtag_limit: int = 5):
    return fetch(token, 'get', 'search', {'userLimit': user_limit, 'hashtagLimit': hashtag_limit, 'q': query})
import requests


def post_user(user, animeid, rating):
    user_rating = {'user': user, 'animeid': animeid, 'rating': rating}
    url = "http://127.0.0.1:5000/users"

    response = requests.post(url, data = user_rating)

    print(response.text)
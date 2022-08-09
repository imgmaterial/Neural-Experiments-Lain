import requests

headers = {"User-Agent": "Api Test"}

def get_user_rates(user):
    url = "https://shikimori.one/api/v2/user_rates"
    data = {"user_id":str(user)}
    response = requests.get(url,data=data, headers=headers)
    return response.json()

def clear_rates(user):
    clean_data = []
    ini_data = get_user_rates(user)
    for i in range(len(ini_data)):
        data = ini_data[i]
        rating_clean = []
        rating_clean.append(data['user_id'])
        rating_clean.append(data['target_id'])
        rating_clean.append(data['score'])
        clean_data.append(rating_clean)
    return(clean_data)

def get_user_id(username):
    url = "https://shikimori.one/api/users/" + str(username)
    data = {"is_nickname":1}
    response = requests.get(url,data=data, headers=headers)
    return response.json()['id']

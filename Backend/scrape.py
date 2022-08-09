import requests
from bs4 import BeautifulSoup
import rec
import sys

def translate(user):
    rec_list = rec.get_preds_for_user(user)
    translate_list = []
    for i in range(len(rec_list)):
        link = 'https://myanimelist.net/anime/' + str(rec_list[i][0])
        response = requests.get(link)
        soup = BeautifulSoup(response.text, 'html.parser')
        if soup.find(class_ = 'h1-title') == None:
            print('empty')
        else:
            title = soup.find(class_ = 'h1-title').get_text()
            translate_list.append([rec_list[i][0],title,rec_list[i][1]])
            print(rec_list[i][0],title,rec_list[i][1])
    return(translate_list)



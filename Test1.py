from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import time
import openpyxl
import pandas as pd

def all_d(url):
    mylist = list() #[0]-Название [1]- дата выхода [2]- Рейтинг IMDB [3]- Рейтинг КП [4]- Рейтин Критиков [5]- Длительность (мин)[6]- Описание
    req = requests.get(url).text
    soup = BeautifulSoup(req, 'lxml')
    #Название
    try:
        title = soup.find("h1", {"class" : "film-page__title-text film-page__itemprop"}).text
        mylist.append(str(title))
    except:
        print("Ошибка в выгрузке названия)")
        mylist.append(str("Ошибка в выгрузке названия) "+url))
   
    #Дата выхода
    try:
        date = soup.find("span", {"class" : "data film-page__date"}).text[2:-2]
        mylist.append(int(date))
    except:
        print("Ошибка в выгрузке даты выхода")  
        mylist.append(str("Ошибка в выгрузке даты выхода "+ url))

    #Рейтинг IMDB
    try:
        imdb = (soup.find("a", {"class" : "noLink ratingsBlockIMDb"}).text[:9])[6:]
        mylist.append(float(imdb))
    except:
        print("Ошибка Рейтинг IMDB") 
        mylist.append(str("Ошибка Рейтинг IMDB " + url))

    #Рейтинг КП
    try:
        kp = (soup.find("a", {"class" : "noLink ratingsBlockKP"}).text[:13])[10:]
        mylist.append(float(kp))
    except:
        print("Ошибка Рейтинг Кинопоиск")
        mylist.append(str("Ошибка Рейтинг Кинопоиск " + url))

    #Рейтинг Кинокритиков
    try:
        critik = soup.find("ul", {"class" : "ratingsBlock"}).text.split('Критики')[-1].strip()[:2]
        mylist.append(int(critik))
    except:
        print("Ошибка блок 5 (Рейтинг Критиков)")  
        mylist.append(str("Ошибка блок 5 (Рейтинг Критиков) " + url))

    #Длительность
    try:    
        min1 = soup.find("div", {"class" : "film-page__infowrap"}).text.split('премьера')
        min2 = min1[0].split('длительность')
        try:
            min3 = min2[1].strip().split("ч")
            hours = int(min3[0])
            minute = int(min3[1].strip()[:2])
            mylist.append(int(hours*60+minute))
        except:
            minute = min2[1].strip()[:2]
            mylist.append(int(minute))      
    except:
            print("Ошибка в загрузке длительности")
            mylist.append(str("Ошибка в загрузке длительности" + url))
    
    #Описание 
    try:
        desc = soup.find("section", {"class" : "text film-page__text"}).text[10:]
        mylist.append(desc)      
    except:
        print("Ошибка в загрузке описания")
        mylist.append(str("Ошибка в загрузке описания" + url))

    #Жанры
    mylist_genre = list()
    try:
        for el in soup.find_all("li", {"itemprop" : "genre"}):
            mylist_genre.append(str(el.get_text()))
    except:
        print("Ошибка в загрузке жанров")
        mylist_genre.append(str("Ошибка в загрузке жанров "+url))


    #Страна 
    mylist_country = list()
    try:
        country = soup.find("div", {"class" : "film-page__infowrap"}).text.split('длительность')
        country2 = country[0].strip()[9:].strip().split(',')
        mylist_country = country2

    except:
        print("Ошибка в загрузке стран")
        mylist_country.append(str("Ошибка в загрузке стран "+url))


    #Ключевые слова 
    try:
        words = soup.find("div", {"class" : "film-page__adjective-list"}).text
        mylist_words2=words.replace(".", "").split("•")
        #print(words2)
    except:
        print("Ошибка в загрузке похожих слов")
    #Похожие фильмы 
    mylist_similar = list()
    count = 0
    try:
        similar_film = soup.find_all("div", {"class" : "poster statusWidgetData no_status"})
        for el in similar_film:
            el1 = str(el).split('data-moviename=')
            el2 = el1[1].split('"')
            if count < 10:
                mylist_similar.append(str(el2[1]))

            count= count + 1
            #print("--------------/n")
    except:
        print("Ошибка в загрузке похожих фильмов")
    
    #Актеры + #Режисеры 
    mylist_actors = list()
    mylist_directors = list()
    url_new = url + "cast/"
    req2 = requests.get(url_new).text
    soup2 = BeautifulSoup(req2, 'lxml')
    try:
        act1 = soup2.find("div",{"class" : "cast-page__items cast-page__items_actor crew-wrap headlines__wrap headlines__wrap_show"}) 
        act2 = act1.find_all("h5", {"class" : "cast-page__item-name"})
        if len(act2) < 10:
            range_of = len(act2)
        else:
            range_of = 10
        for i in range(range_of):
            mylist_actors.append(str(act2[i].get_text()))
    except:
        print("Ошибка в загрузке актеров")
        mylist_actors.append(str("Ошибка в загрузке актеров "+url))

    try:
        directors1 = soup2.find("div",{"class" : "cast-page__items cast-page__items_director cast-page__items_grid crew-wrap headlines__wrap headlines__wrap_show"}) 
        directors2 = directors1.find_all("h5", {"class" : "cast-page__item-name"})
        for i in range(len(directors2)):
            mylist_directors.append(str(directors2[i].get_text()))
    except:
        print("Ошибка в загрузке режиссеров")
        mylist_directors.append(str("Ошибка в загрузке режиссеров "+url))

    print("test________")
    data_all = {'id': [],
        'url': [],
        'title': [],
        'date': [],
        'imdb': [],
        'kp': [],
        'critik': [],
        'minute': [],
        'desc': [],
        'genre': [],
        'actors': [],
        'director': [],
        'country': [],
        'similar': [],
        'words2': []}
    
    data_all["url"].append(str(url))
    data_all["title"].append(mylist[0])
    data_all["date"].append(mylist[1])
    data_all["imdb"].append(mylist[2])
    data_all["kp"].append(mylist[3])
    data_all["critik"].append(mylist[4])
    data_all["minute"].append(mylist[5])
    data_all["desc"].append(mylist[6])
    data_all["genre"].append(mylist_genre)
    data_all["actors"].append(mylist_actors)
    data_all["director"].append(mylist_directors)
    data_all["country"].append(mylist_country)
    data_all["similar"].append(mylist_similar)
    data_all["words2"].append(mylist_words2)

    print(data_all)
    return data_all
  


    #Фото постера
    '''
    try:
        link_logo = str(soup.find("div", {"class" : "carousel_image-handler image_block carousel_image-handler_pointer"})).split('"')
        name = str(title)
        print(link_logo[9])
        url2=str(link_logo[9])
        img = requests.get(url2)
        img_option = open(name + '.jpg', 'wb')
        img_option.write(img.content)
        img_option.close()   
    except:
        print("Ошибка при загрузке логотипа")  
    ''' 

def main():
    url = 'https://ru.kinorium.com/101209/'
    id_1 = 101209
    url_2= 'https://ru.kinorium.com/1630764/'
    url_3= 'https://ru.kinorium.com/315263/'
    url_4='https://ru.kinorium.com/101209/cast/'
    url_5 = 'https://ru.kinorium.com/479385/'
    #all_d(url)
    all_d(url)
    #df = pd.DataFrame(all_d(url))
    #file_name = 'example5.xlsx'
    #df.to_excel(file_name, index=False)
    #print("test________2")
if __name__ == "__main__":
    main()

import requests
from bs4 import BeautifulSoup
import re
import datetime

from matplotlib import pyplot as plt
from wordcloud import WordCloud

#parsing the site https://www.rbc.ua/rus/allnews (https://www.rbc.ua/rus/archive/2022/12/24)
def parsing_rbc(date):
    if len(str(date.day)) == 1:
        day = '0' + str(date.day)
        day2 = '0' + str(date.day - 1)
    else:
        day = str(date.day)
        day2 = str(date.day - 1)
    if len(str(date.month)) == 1:
        month = '0' + str(date.month)
    else:
        month = str(date.month)
    url1 = 'https://www.rbc.ua/rus/archive/' + str(date.year) + '/' + month + '/' + day
    url2 = 'https://www.rbc.ua/rus/archive/' + str(date.year) + '/' + month + '/' + day2

    #dictionary date:article
    rbc_dict = {}

    # site parsing for the previous date
    r = requests.get(url2)
    soup = BeautifulSoup(r.text, 'html.parser')
    articles = soup.find('div', class_='newsline')

    for article in articles.find_all('div'):
        title = article.find('a').text.replace('\n', '')
        date_article = article.find('span', class_='time').text

        if len(str(date.hour)) == 1 and len(str(date.minute)) == 1:
            if date_article < '0' + str(date.hour) + ':' + '0' + str(date.minute):
                continue
        elif len(str(date.hour)) == 1:
            if date_article < '0' + str(date.hour) + ':' + str(date.minute):
                continue
        elif len(str(date.minute)) == 1:
            if date_article < str(date.hour) + ':' + '0' + str(date.minute):
                continue
        else:
            if date_article < str(date.hour) + ':' + str(date.minute):
                continue

        rbc_dict[date_article + ' ' + day2 + '.' + month + '.' + str(date.year)] = title[5:]

    #site parsing for the current date
    r = requests.get(url1)
    soup = BeautifulSoup(r.text, 'html.parser')

    #get list of articles
    articles = soup.find('div', class_='newsline')
    #until the end of the list get titles and date

    for article in articles.find_all('div'):
        title = article.find('a').text.replace('\n', '')
        date_article = article.find('span', class_='time').text
        rbc_dict[date_article+' '+day+'.'+month+'.'+str(date.year)] = title[5:]

    return rbc_dict

#https://www.pravda.com.ua/news/ (https://www.pravda.com.ua/news/date_24122022/)
def parsing_pravda(date):
    if len(str(date.day)) == 1:
        day = '0' + str(date.day)
        day2 = '0' + str(date.day - 1)
    else:
        day = str(date.day)
        day2 = str(date.day - 1)
    if len(str(date.month)) == 1:
        month = '0' + str(date.month)
    else:
        month = str(date.month)

    url2 = 'https://www.pravda.com.ua/news/date_' + day2 + month + str(date.year) + '/'
    url1 = 'https://www.pravda.com.ua/news/date_' + day + month + str(date.year) + '/'

    pravda_dict = {}

    # site parsing for the previous date
    r = requests.get(url2)
    soup = BeautifulSoup(r.text, 'html.parser')
    articles = soup.find('div', class_='container_sub_news_list_wrapper mode1')
    #remove all <em> tags
    for em in articles.find_all('em'):
        em.decompose()

    for article in articles.find_all('div', class_='article_news_list')[::-1]:
        try:
            title = article.find('div', class_='article_header').text
            date_article = article.find('div', class_='article_time').text

            if len(str(date.hour)) == 1 and len(str(date.minute)) == 1:
                if date_article < '0' + str(date.hour) + ':' +'0'+ str(date.minute):
                    continue
            elif len(str(date.hour)) == 1:
                if date_article < '0' + str(date.hour) + ':' + str(date.minute):
                    continue
            elif len(str(date.minute)) == 1:
                if date_article < str(date.hour) + ':' + '0' + str(date.minute):
                    continue
            else:
                if date_article < str(date.hour) + ':' + str(date.minute):
                    continue

            pravda_dict[date_article + ' ' + day2 + '.' + month + '.' + str(date.year)] = title
        except:
            print('Err')

    # site parsing for the current date
    r = requests.get(url1)
    soup = BeautifulSoup(r.text, 'html.parser')
    articles = soup.find('div', class_='container_sub_news_list_wrapper mode1')
    # remove all <em> tags
    for em in articles.find_all('em'):
        em.decompose()

    for article in articles.find_all('div', class_='article_news_list')[::-1]:
        try:
            title = article.find('div', class_='article_header').text
            date_article = article.find('div', class_='article_time').text

            if len(str(date.hour)) == 1 and len(str(date.minute)) == 1:
                if date_article > '0' + str(date.hour) + ':' +'0'+ str(date.minute):
                    continue
            elif len(str(date.hour)) == 1:
                if date_article > '0' + str(date.hour) + ':' + str(date.minute):
                    continue
            elif len(str(date.minute)) == 1:
                if date_article > str(date.hour) + ':' + '0' + str(date.minute):
                    continue
            else:
                if date_article > str(date.hour) + ':' + str(date.minute):
                    continue

            pravda_dict[date_article + ' ' + day + '.' + month + '.' + str(date.year)] = title
        except:
            print('Err')

    return pravda_dict

#https://www.unian.ua/ (https://www.unian.ua/news/archive) https://www.unian.ua/news/archive/20221223
def parsing_unian(date):
    if len(str(date.day)) == 1:
        day = '0' + str(date.day)
        day2 = '0' + str(date.day - 1)
    else:
        day = str(date.day)
        day2 = str(date.day - 1)
    if len(str(date.month)) == 1:
        month = '0' + str(date.month)
    else:
        month = str(date.month)

    url2 = 'https://www.unian.ua/news/archive/' + str(date.year) + month + day2
    url1 = 'https://www.unian.ua/news/archive/'

    unian_dict = {}

    # site parsing for the previous date
    r = requests.get(url2)
    soup = BeautifulSoup(r.text, 'html.parser')
    articles = soup.find('div', class_='col-md-8 col-sm-12 px-40')
    #title list-thumbs__item  date list-thumbs__time time
    titles = articles.find_all('div', class_='list-thumbs__item')
    dates = articles.find_all('div', class_='list-thumbs__time time')
    for title, date_article in zip(titles[::-1], dates[::-1]):

        if len(str(date.hour)) == 1 and len(str(date.minute)) == 1:
            if date_article.text[:5] < '0' + str(date.hour) + ':' +'0'+ str(date.minute):
                continue
        elif len(str(date.hour)) == 1:
            if date_article.text[:5] < '0' + str(date.hour) + ':' + str(date.minute):
                continue
        elif len(str(date.minute)) == 1:
            if date_article.text[:5] < str(date.hour) + ':' + '0' + str(date.minute):
                continue
        else:
            if date_article.text[:5] < str(date.hour) + ':' + str(date.minute):
                continue

        unian_dict[date_article.text[:5] + ' ' + day2 + '.' + month + '.' + str(date.year)] = \
            title.text.replace('\n', '')

    # site parsing for the current date
    r = requests.get(url1)
    soup = BeautifulSoup(r.text, 'html.parser')
    articles = soup.find('div', class_='col-md-8 col-sm-12 px-40')
    # title list-thumbs__item  date list-thumbs__time time
    titles = articles.find_all('div', class_='list-thumbs__item')
    dates = articles.find_all('div', class_='list-thumbs__time time')
    for title, date_article in zip(titles[::-1], dates[::-1]):
        unian_dict[date_article.text[:5] + ' ' + day + '.' + month + '.' + str(date.year)] = \
            title.text.replace('\n', '')

    #clear headers
    for key, value in unian_dict.items():
        index = value.find(key[0:5])
        unian_dict[key] = value[:index]

    return unian_dict

#https://24tv.ua/archive/23_december_2022/

def parsing_24tv(date):
    if len(str(date.day)) == 1:
        day = '0' + str(date.day)
        day2 = '0' + str(date.day - 1)
    else:
        day = str(date.day)
        day2 = str(date.day - 1)
    if len(str(date.month)) == 1:
        month = '0' + str(date.month)
    else:
        month = str(date.month)

    name_month = {1: 'january', 2: 'february', 3: 'march', 4: 'april', 5: 'may', 6: 'june', 7: 'july', 8: 'august',
                  9: 'september', 10: 'october', 11: 'november', 12: 'december'}

    url2 = 'https://24tv.ua/archive/' + day2 + '_' + name_month[date.month] + '_' + str(date.year) + '/'
    url1 = 'https://24tv.ua/archive/' + day + '_' + name_month[date.month] + '_' + str(date.year) + '/'

    tv24_dict = {}

    # site parsing for the previous date
    r = requests.get(url2)
    soup = BeautifulSoup(r.text, 'html.parser')
    articles = soup.find('ul', class_='clear-list news-list-wrapper')

    titles = articles.find_all('div', class_='news-title')
    dates = articles.find_all('div', class_='time')

    for title, date_article in zip(titles, dates):

        if len(str(date.hour)) == 1 and len(str(date.minute)) == 1:
            if date_article.text[:5] < '0' + str(date.hour) + ':' +'0'+ str(date.minute):
                continue
        elif len(str(date.hour)) == 1:
            if date_article.text[:5] < '0' + str(date.hour) + ':' + str(date.minute):
                continue
        elif len(str(date.minute)) == 1:
            if date_article.text[:5] < str(date.hour) + ':' + '0' + str(date.minute):
                continue
        else:
            if date_article.text[:5] < str(date.hour) + ':' + str(date.minute):
                continue

        tv24_dict[date_article.text[:5] + ' ' + day2 + '.' + month + '.' + str(date.year)] = \
            title.text.replace('\n', '')

    # site parsing for the current date
    r = requests.get(url1)
    soup = BeautifulSoup(r.text, 'html.parser')
    articles = soup.find('ul', class_='clear-list news-list-wrapper')

    titles = articles.find_all('div', class_='news-title')
    dates = articles.find_all('div', class_='time')

    for title, date_article in zip(titles, dates):
        tv24_dict[date_article.text[:5] + ' ' + day + '.' + month + '.' + str(date.year)] = \
            title.text.replace('\n', '')

    return tv24_dict

def parsing_all(date):
    if len(str(date.day)) == 1:
        day = '0' + str(date.day)
        day2 = '0' + str(date.day - 1)
    else:
        day = str(date.day)
        day2 = str(date.day - 1)
    if len(str(date.month)) == 1:
        month = '0' + str(date.month)
    else:
        month = str(date.month)

    rbc_dict = parsing_rbc(date)
    pravda_dict = parsing_pravda(date)
    unian_dict = parsing_unian(date)
    tv24_dict = parsing_24tv(date)

    #combine dictionaries, if the key is the same, write it down with a space
    all_dict = {}
    for key, value in rbc_dict.items():
        all_dict[key] = value
    for key, value in pravda_dict.items():
        if key in all_dict:
            all_dict[key] += ' | ' + value
        else:
            all_dict[key] = value
    for key, value in unian_dict.items():
        if key in all_dict:
            all_dict[key] += ' | ' + value
        else:
            all_dict[key] = value
    for key, value in tv24_dict.items():
        if key in all_dict:
            all_dict[key] += ' | ' + value
        else:
            all_dict[key] = value

    #sort by key[6:8]
    all_dict = dict(sorted(all_dict.items(), key=lambda item: item[0][6:8]))

    #split into 2 dictionaries for key[6:8] = date.day and key[6:8] = date.day - 1
    all_dict1 = {}
    all_dict2 = {}
    for key, value in all_dict.items():
        if key[6:8] == day:
            all_dict1[key] = value
        else:
            all_dict2[key] = value

    #sort by key[0:5]
    all_dict1 = dict(sorted(all_dict1.items(), key=lambda item: item[0][0:5]))
    all_dict2 = dict(sorted(all_dict2.items(), key=lambda item: item[0][0:5]))

    all_dict = {**all_dict2, **all_dict1}

    #clear the file
    with open('news.txt', 'w') as file:
        file.write('')
    #write to a file
    with open('news.txt', 'w', encoding='utf-8') as file:
        for key, value in all_dict.items():
            file.write(key + ' ' + value + '\n')

    return all_dict, rbc_dict, pravda_dict, unian_dict, tv24_dict

#analysis
def analysis(input_dict, title, type):
    if len(str(date.day)) == 1:
        day = '0' + str(date.day)
        day2 = '0' + str(date.day - 1)
    else:
        day = str(date.day)
        day2 = str(date.day - 1)
    if len(str(date.month)) == 1:
        month = '0' + str(date.month)
    else:
        month = str(date.month)
    #split into 24 dictionaries by hours date.hour date.day-1 - date.hour date.day
    dict_24 = {}
    kolvo_novostey = [0] * 24
    for key, value in input_dict.items():
        if key[0:2]+' '+key[6:8] not in dict_24:
            dict_24[key[0:3]+' '+key[6:8]] = {}

    for key, value in input_dict.items():
        dict_24[key[0:3]+' '+key[6:8]] = str(dict_24[key[0:3]+' '+key[6:8]]) + input_dict[key] + ' | '
        if key[6:8] == day2:
            kolvo_novostey[int(key[0:2])-int(date.hour)-1] += 1
        elif key[6:8] == day:
            kolvo_novostey[int(24-int(date.hour)+int(key[0:2])-1)] += 1


    for key, value in dict_24.items():
        dict_24[key] = str(dict_24[key])[2:]

    xnames = []
    for i in range(date.hour, 23):
        xnames.append(str(i)+ '-'+ str(i+1))
    for i in range(0, date.hour + 1):
        xnames.append(str(i)+'-'+ str(i+1))

    if type == 1:
        plt.bar(range(len(kolvo_novostey)), kolvo_novostey)
        plt.xticks(range(24), xnames, rotation=60)
        plt.title('Зміна кількості новин по годинам у період '+day2+'.'+month+
                  '.'+str(date.year)+' - '+ day+'.'+month+'.'+str(date.year)+'\n'+title)
        plt.show()

    words = []
    for key, value in dict_24.items():
        words.append(value)

    stop_words = [' і ', ' та ', ' що ', ' в ', ' на ', ' з ', ' до ', ' з ', ' за ', ' а ', ' або ', ' як ', ' не ', ' що ',
    ' щоб ', ' якщо ', ' коли ', ' але ', ' аби ', ' якби ', ' бо ', ' б ', ' би ', ' у ', ' їх ', ' її ', ' їй ', ' їм ', ' їх ',
    ' про ', ' по ', 'під', ' У ', ' В ', ' З ', ' І ', ' Та ', ' Що ', ' На ', ' До ', ' За ', ' А ', ' Або ', ' Як ', ' Не ', ' Що ',
    ' Щоб ', ' Якщо ', ' Коли ', ' Але ', ' Аби ', ' Якби ', ' Бо ', ' Б ', ' Би ', ' У ', ' Їх ', ' Її ', ' Їй ', ' Їм ', ' Їх ',
    ' Про ', ' По ', 'Під', ' після ', ' через ', ' від ', ' яка ', ' які ', ' яку ', ' якого ', ' якому ', ' яким ', ' якими ', ' якій ']

    for i in range(len(words)):
        for j in range(len(stop_words)):
            #видалити не враховуючи регістру
            words[i] = words[i].replace(stop_words[j], ' ')

    #видалити знаки регулярними виразами
    for i in range(len(words)):
        words[i] = re.sub(r'[^\w\s]', '', words[i])
    #видалити цифри
    for i in range(len(words)):
        words[i] = re.sub(r'\d', '', words[i])

    if type == 1:
        wordcloud = WordCloud(width=1000, height=1000, background_color='white', min_font_size=10).generate(str(words))
        plt.figure(figsize=(8, 8), facecolor=None)
        plt.imshow(wordcloud)
        plt.axis("off")
        plt.tight_layout(pad=2)
        plt.title('Популярні слова у новинах з усіх сайтів')
        plt.show()

    return kolvo_novostey, xnames, words

date = datetime.datetime.now()
all_dict, rbc_dict, pravda_dict, unian_dict, tv24_dict = parsing_all(date)
analysis(all_dict, 'Збірка новин з усіх 4 сайтів', 1)

def graph_4_sources(rbc_dict, pravda_dict, unian_dict, tv24_dict):
    #plot graphs for each site
    rbc_kolvo_novostey, rbc_xnames, rbc_words = analysis(rbc_dict, 'Новини з сайту RBC', 0)
    pra_kolvo_novostey, pra_xnames, pra_words = analysis(pravda_dict, 'Новини з сайту Pravda', 0)
    unian_kolvo_novostey, unian_xnames, unian_words = analysis(unian_dict, 'Новини з сайту Уніан', 0)
    tv24_kolvo_novostey, tv24_xnames, tv24_words = analysis(tv24_dict, 'Новини з сайту Україна24', 0)

    figure = plt.figure()
    ax = figure.add_subplot(111, projection='3d')
    #x - hours, y - sites, z - number of news, 3d column
    ax.bar(range(24), rbc_kolvo_novostey, 3, zdir='y', color='r', width=0.5, label='RBC')
    ax.bar(range(24), unian_kolvo_novostey, 2, zdir='y', color='b', width=0.5, label='Уніан')
    ax.bar(range(24), pra_kolvo_novostey, 1, zdir='y', color='g', width=0.5, label='Правда')
    ax.bar(range(24), tv24_kolvo_novostey, 4, zdir='y', color='y', width=0.5, label='Україна24')
    ax.set_xlabel('Години')
    ax.set_zlabel('Кількість новин')
    ax.set_yticks([1, 2, 3, 4])
    ax.set_xticks(range(24))
    ax.set_xticklabels(rbc_xnames, rotation=35, fontsize=8, rotation_mode='anchor', wrap=True,)
    plt.legend()
    plt.show()

    #plot graphs for each site
    wordcloud = WordCloud(width=1000, height=1000, background_color='white', min_font_size=10).generate(str(rbc_words))
    plt.figure(figsize = (8, 8), facecolor = None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad = 2)
    plt.title('Популярні слова з новин з сайту RBC')
    plt.show()

    wordcloud = WordCloud(width=1000, height=1000, background_color='white', min_font_size=10).generate(str(pra_words))
    plt.figure(figsize = (8, 8), facecolor = None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad = 2)
    plt.title('Популярні слова з новин з сайту Pravda')
    plt.show()

    wordcloud = WordCloud(width=1000, height=1000, background_color='white', min_font_size=10).generate(str(unian_words))
    plt.figure(figsize = (8, 8), facecolor = None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad = 2)
    plt.title('Популярні слова з новин з сайту Уніан')
    plt.show()

    wordcloud = WordCloud(width=1000, height=1000, background_color='white', min_font_size=10).generate(str(tv24_words))
    plt.figure(figsize = (8, 8), facecolor = None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad = 2)
    plt.title('Популярні слова з новин з сайту Україна24')
    plt.show()

graph_4_sources(rbc_dict, pravda_dict, unian_dict, tv24_dict)
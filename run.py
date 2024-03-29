#!/usr/bin/python

import requests
from bs4 import BeautifulSoup as BS
import time
import datetime
import sqlite3
from aiogram.utils import executor
from aiogram import Bot, Dispatcher


def get_requests(url, base_url, selector, metod=''):
    new = ''
    try:
        print(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + ' Получение страницы: ' + url)
        while not len(new):
            if metod == 'post':
                answ = s.post(url, data=postdata, headers=headers)
            else:
                answ = s.get(url, headers=headers)

            ans_bs = BS(answ.content, 'html.parser')
            new = ans_bs.select(selector)

            print(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + " Ссылок на странице: " + str(len(new)))

            if len(new):
                for elem in new:
                    new_link[base_url + elem.attrs['href']] = elem.text
            else:
                time.sleep(61)
                print(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + 'Ожидание 1 мин')
    finally:
        pass


API_TOKEN = '***********'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


async def send_telegram(links={}):
    for elem in links:
        await bot.send_message(297036937, elem)


new_link = {}
send_link = {}

s = requests.Session()
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,la;q=0.6',
    'cache-control': 'max-age=0',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36'
}
postdata = {
    'action': 'postfilter',
    'kind': '5',
    'pf_category': '',
    'pf_subcategory': '',
    'comboe_columns%5B1%5D': '0',
    'comboe_columns%5B0%5D': '0',
    'comboe_column_id': '0',
    'comboe_db_id': '0',
    'comboe': '%D0%92%D1%81%D0%B5+%D1%81%D0%BF%D0%B5%D1%86%D0%B8%D0%B0%D0%BB%D0%B8%D0%B7%D0%B0%D1%86%D0%B8%D0%B8',
    'location_columns%5B1%5D': '0',
    'location_columns%5B0%5D': '0',
    'location_column_id': '0',
    'location_db_id': '0',
    'location': '%D0%92%D1%81%D0%B5+%D1%81%D1%82%D1%80%D0%B0%D0%BD%D1%8B',
    'hide_exec': '1',
    'pf_cost_from': '',
    #    'pf_cost_from': '5000',
    'pf_cost_to': '',
    #   'pf_cost_to': '70000',
    'u_token_key': 'a8dcb7e72c80fef5394da9732d04e9d9'
}

i = -1
while int(datetime.datetime.now().strftime("%H")) != 0:
    i += 1
    # print('fl', i)
    # postdata['pf_keywords'] = 'python'
    # get_requests('https://www.fl.ru/projects/', 'https://www.fl.ru', 'a.b-post__link', 'post')
    postdata['pf_keywords'] = 'django'
    get_requests('https://www.fl.ru/projects/', 'https://www.fl.ru', 'a.b-post__link', 'post')
#    time.sleep(151)
#    postdata['pf_keywords'] = 'react'
#    get_requests('https://www.fl.ru/projects/', 'https://www.fl.ru', 'a.b-post__link', 'post')
    time.sleep(301)

    if i % 6 == 0:
        # print('all')
        # get_requests('https://krasnodar.hh.ru/search/vacancy?search_period=7&clusters=true&area=1438&text=Python&order_by=publication_time&enable_snippets=true', '', 'a.bloko-link.HH-LinkModifier')
        get_requests('https://krasnodar.hh.ru/search/vacancy?clusters=true&enable_snippets=true&order_by=publication_time&schedule=remote&search_period=3&text=Python&L_save_area=true&area=113&from=cluster_area&showClusters=true', '', 'a.bloko-link.HH-LinkModifier')
        # get_requests('https://career.habr.com/vacancies?city_id=707&type=all', 'https://career.habr.com/', 'div.vacancy-card__title>a')
        get_requests('https://career.habr.com/vacancies?q=python&remote=true&type=all', 'https://career.habr.com/', 'div.vacancy-card__title>a')
        get_requests('https://russia.superjob.ru/vacancy/search/?keywords=python&remote_work=1', 'https://russia.superjob.ru', 'a._1UJAN')
        get_requests('https://rabota.yandex.ru/krasnodarskiy_kray/vakansii/?text=python&top_days=7&sort=cr_date', '', 'a.link.serp-vacancy__name.stat__click')
        postdata['pf_keywords'] = 'fastapi'
        get_requests('https://www.fl.ru/projects/', 'https://www.fl.ru', 'a.b-post__link', 'post')
        time.sleep(151)

    for link in new_link:

        conn = sqlite3.connect('mydatabase.db')

        cursorObj = conn.cursor()
        cursorObj.execute("CREATE TABLE if not exists vacancy(url text PRIMARY KEY, title text , create_datetime text)")
        cursorObj.execute("SELECT url FROM vacancy WHERE url = :link", {"link": link})

        row = cursorObj.fetchone()
        if None == row:
            cursorObj.execute("INSERT INTO vacancy VALUES (?, ?, DateTime('now', 'localtime'))", (link, new_link[link]))
            conn.commit()
            print(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + ' ' + link, new_link[link])

            send_link[link] = new_link[link]
            time.sleep(8)
        conn.close()

    try:
        executor.start(dp, send_telegram(send_link))
    except:
        print('telegramm not connected')

    new_link.clear()
    send_link.clear()

    if 9 <= int(datetime.datetime.now().strftime("%H")) <= 22:
        print(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + ' Ожидание 5 мин')
        # time.sleep(301)
    else:
        print(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + ' Ожидание 20 мин')
        time.sleep(901)

''' Скрипт для уведомлений о новых вакансиях '''
import requests
from bs4 import BeautifulSoup as BS
import time
import sqlite3
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def get_requests(url, base_url, selector, metod=''):
    if metod == 'post':
        answ = s.post(url, data=postdata, headers=headers)
    else:
        answ = s.get(url, headers=headers)
    ans_bs = BS(answ.content, 'html.parser')
    new = ans_bs.select(selector)
    for elem in new:
        new_link[base_url + elem.attrs['href']] = elem.text

def send_mail(links={}):
    addr_from = "bez1dn6a@mail.ru"                      # Адресат
    addr_to = "bez1dn6a@yandex.ru"                      # Получатель
    password = "\\\ пароль скрыт ///"                   # Пароль
    msg = MIMEMultipart()                               # Создаем сообщение
    msg['From'] = addr_from                             # Адресат
    msg['To'] = addr_to                                 # Получатель
    msg['Subject'] = 'Ссылки по работе'                 # Тема сообщения
    html = """
    <html>
      <head></head>
      <body>"""
    for elem in links:
        html = html + '<a href="' + elem + '">' + links[elem] + '</a><br>'
    html = html + """
      </body>
    </html>
    """
    msg.attach(MIMEText(html, 'html', 'utf-8'))         # Добавляем в сообщение HTML-фрагмент
    server = smtplib.SMTP('smtp.mail.ru', 25)           # Создаем объект SMTP
    server.set_debuglevel(False)                        # Выключаем режим отладки
    server.starttls()                                   # Начинаем шифрованный обмен по TLS
    server.login(addr_from, password)                   # Получаем доступ
    server.send_message(msg)                            # Отправляем сообщение
    server.quit()                                       # Выходим


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
    'pf_cost_from': '5000',
    'pf_cost_to': '',
    'u_token_key': 'a8dcb7e72c80fef5394da9732d04e9d9'
}


i = -1
while 1:
    i += 1
    if i % 4 == 0:
        print('all')
        get_requests('https://krasnodar.hh.ru/search/vacancy?search_period=7&clusters=true&area=1438&text=Python&order_by=publication_time&enable_snippets=true', '', 'a.bloko-link.HH-LinkModifier')
        get_requests('https://krasnodar.hh.ru/search/vacancy?clusters=true&enable_snippets=true&order_by=publication_time&schedule=remote&search_period=3&text=Python&L_save_area=true&area=113&from=cluster_area&showClusters=true', '', 'a.bloko-link.HH-LinkModifier')
        get_requests('https://career.habr.com/vacancies?city_id=707&type=all', 'https://career.habr.com/', 'div.vacancy-card__title>a')
        get_requests('https://career.habr.com/vacancies?q=python&remote=true&type=all', 'https://career.habr.com/', 'div.vacancy-card__title>a')
        get_requests('https://russia.superjob.ru/vacancy/search/?keywords=python&remote_work=1', 'https://russia.superjob.ru', 'a._1UJAN')
        get_requests('https://rabota.yandex.ru/krasnodarskiy_kray/vakansii/?text=python&top_days=7&sort=cr_date', '', 'a.link.serp-vacancy__name.stat__click')
    print(i, 'fl')
    postdata['pf_keywords'] = 'python'
    get_requests('https://www.fl.ru/projects/', 'https://www.fl.ru', 'a.b-post__link', 'post')
    postdata['pf_keywords'] = 'django'
    get_requests('https://www.fl.ru/projects/', 'https://www.fl.ru','a.b-post__link', 'post')

    for link in new_link:

        conn = sqlite3.connect('mydatabase.db')

        cursorObj = conn.cursor()
        # cursorObj.execute("CREATE TABLE if not exists vacancy(url text PRIMARY KEY, title text )")
        cursorObj.execute("SELECT url FROM vacancy WHERE url = :link", {"link": link})

        row = cursorObj.fetchone()
        if None == row:
            cursorObj.execute("INSERT INTO vacancy VALUES (?, ?)", (link, new_link[link]))
            conn.commit()
            print(link, new_link[link])
            send_link[link] = new_link[link]
        conn.close()

    send_mail(send_link)
    new_link.clear()
    send_link.clear()

    time.sleep(300)

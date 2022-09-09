import requests
from bs4 import BeautifulSoup


headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.160 YaBrowser/22.5.3.673 Yowser/2.5 Safari/537.36"
}


def get_subcategory(POSTSOUD):
    perl = POSTSOUD.find(class_='kroshki').find_all('a')
    # print(perl[1].text)
    return perl[1].text


def get_img(POSTSOUD):
    posts = POSTSOUD.find('div', class_='vacancy_item_block').find_all('img')
    if posts:
        # print("Изоб    ", 'http:' + posts[0]['src'])
        return 'http:' + posts[0]['src']

def get_title(POSTSOUD):
    title = POSTSOUD.find(class_='title')
    if title:
        # print('Название   ', title.text)
        return title.text


def get_town(POSTSOUD):
    town = POSTSOUD.find(class_='title').findNext()

    if town:
        # print('Город   ', town.text)
        return town.tex


def get_price(POSTSOUD):
    price = POSTSOUD.find(class_='price')
    if price:
        # print(price.text)
        return price.text


def get_number(POSTSOUD):
    number = POSTSOUD.find(class_='desc')

    if number:
        if len(number.text.strip().split()) >= 4:
            # print('Номер', *number.text.strip().split()[1:-2])
            return "".join(number.text.strip().split()[1:-2])
        else:
            # print('Номер', *number.text.strip().split()[1:])
            return ''.join(number.text.strip().split()[1:])

def get_email(POSTSOUD):
    email = POSTSOUD.find(class_='desc')
    if len(email.text.split()) >= 4 and email.text.split()[2] == 'Email:':
        # print('Email', email.text.split()[-1])
        return email.text.split()[-1]


def get_descrition(POSTSOUD):
    desc = POSTSOUD.find_all(class_='desc')
    if desc:
        # print(desc[1].text)
        return desc[1].text


def run_pars():
    list_link_all_posts = ['http://resume.doska.kg/vacancy/&page=2&sortby=new',
                           'http://resume.doska.kg/vacancy/&page=2&sortby=new']

    for j in list_link_all_posts:
        post = requests.get(j, headers=headers)
        postsrc = post.text
        POSTSOUD = BeautifulSoup(postsrc, "lxml")
        deteil_post_links = []
        posts = POSTSOUD.find(class_="mp_last_items_block2").find_all("a")

        for k in posts:
            Iten_href1 = 'http://resume.doska.kg' + k.get("href")
            deteil_post_links.append(Iten_href1)

        list_post_links = deteil_post_links[:-4]

        for i in list_post_links:
            post = requests.get(i, headers=headers)
            postsrc = post.text
            POSTSOUD = BeautifulSoup(postsrc, "lxml")

            subcategory=get_subcategory(POSTSOUD)
            img=get_img(POSTSOUD)
            title=get_title(POSTSOUD)
            town=get_town(POSTSOUD)
            price=get_price(POSTSOUD)
            number=get_number(POSTSOUD)
            email=get_email(POSTSOUD)
            description=get_descrition(POSTSOUD)



            # print('---------------------')

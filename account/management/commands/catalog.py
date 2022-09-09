# from account.models import UserProfile
import os

import requests
from bs4 import BeautifulSoup
from django.utils import timezone
from django.core.management import BaseCommand

from account.models import UserProfile
from account.parsing.doska import run_pars
from adds.models import Post, Category, Subcategory

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.160 YaBrowser/22.5.3.673 Yowser/2.5 Safari/537.36"
}


def get_subcategory(POSTSOUD):
    perl = POSTSOUD.find(class_='pathway').find_all('a')
    print(perl[-1].text)
    return perl[-1].text


def get_img(POSTSOUD):
    posts = POSTSOUD.find('div', class_='vacancy_item_block').find_all('img')
    if posts:
        print("Изоб    ", 'http:' + posts[0]['src'])
        return 'http:' + posts[0]['src']


def get_title(POSTSOUD):
    title = POSTSOUD.find(class_='con_heading')
    if title:
        print('Название   ', title.text)
        return title.text


def get_town(POSTSOUD):
    town = POSTSOUD.find(class_='bd_item_city')

    if town:
        print('Город   ', town.text)
        return town.tex


def get_price(POSTSOUD):
    price = POSTSOUD.find(class_='price')
    if price:
        print(price.text)
        return price.text.split()[1]


def get_number(POSTSOUD):
    number = POSTSOUD.find(class_='desc')

    if number:
        if len(number.text.strip().split()) >= 4:
            print('Номер', *number.text.strip().split()[1:-2])
            return "".join(number.text.strip().split()[1:-2])
        else:
            print('Номер', *number.text.strip().split()[1:])
            return ''.join(number.text.strip().split()[1:])


def get_email(POSTSOUD):
    email = POSTSOUD.find(class_='desc')
    if len(email.text.split()) >= 4 and email.text.split()[2] == 'Email:':
        print('Email', email.text.split()[-1])
        return email.text.split()[-1]


def get_descrition(POSTSOUD):
    desc = POSTSOUD.find_all(class_='bd_text_full')
    if desc:
        print(desc[0].text)
        return desc[0].text


def run_pars_catalog():
    me = UserProfile.objects.get(pk=1)
    try:
        Category.objects.create(title='Работа')
    except:
        pass


    count_post = 0

    for l in range(200):

        link_catalog = f'https://www.catalog.kg/board/22-{l}'
        post = requests.get(link_catalog, headers=headers)
        postsrc = post.text

        with open(f'account/management/parsing/{l}.html','w') as file:
            file.write(postsrc)

        with open(f'account/management/parsing/{l}.html') as file:
            postsrc = file.read()


        POSTSOUD = BeautifulSoup(postsrc, "lxml")
        deteil_post_links = []
        posts = POSTSOUD.find(class_="board_gallery").find_all("a")

        for k in posts:
            Iten_href1 = 'https://www.catalog.kg' + k.get("href")
            deteil_post_links.append(Iten_href1)

        list_post_links = deteil_post_links[:-4]


        for i in list_post_links:
            post = requests.get(i, headers=headers)
            postsrc = post.text
            POSTSOUD = BeautifulSoup(postsrc, "lxml")

            subcategory = get_subcategory(POSTSOUD)
            title = get_title(POSTSOUD)
            town = get_town(POSTSOUD)
            description = get_descrition(POSTSOUD)

            category_id = Category.objects.get(title='Работа')

            try:
                subcategory_id = Subcategory.objects.get(title=subcategory)
            except:
                Subcategory.objects.create(category=category_id, title=subcategory)
                subcategory_id = Subcategory.objects.get(title=subcategory)

            try:
                Post.objects.create(user=me, category=category_id,
                                    subcategory=subcategory_id,
                                    title=title,
                                    city=town,
                                   description=description)
                count_post += 1
            except Exception as ex:
                print(ex)
            print(count_post)
            if count_post == 100:
                break

        os.remove(f'account/management/parsing/{l}.html')

        if count_post == 100:
            break


class Command(BaseCommand):
    kali = 'Sos'

    def handle(self, *args, **kwargs):
        time = timezone.now().strftime('%X')
        self.stdout.write("It's now %s" % time)
        run_pars_catalog()
        time = timezone.now().strftime('%X')
        self.stdout.write("It's now %s" % time)

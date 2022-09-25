import os
import urllib.request

import requests
from bs4 import BeautifulSoup
from django.utils import timezone
from django.core.management import BaseCommand

from account.models import User
from adds.models import Post, Category, Subcategory, PostContacts

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.160 YaBrowser/22.5.3.673 Yowser/2.5 Safari/537.36"
}


def get_subcategory(POSTSOUD):
    perl = POSTSOUD.find(class_='kroshki').find_all('a')
    return perl[1].text


def get_img(POSTSOUD):
    posts = POSTSOUD.find('div', class_='vacancy_item_block').find_all('img')
    if posts:
        img_link = 'http:' + posts[0]['src']
        if not os.path.exists('media/images'):
            os.mkdir('media/images')
        img = img_link.split('/')
        urllib.request.urlretrieve(img_link, f'media/images/{img[-1]}')
        return f'images/{img[-1]}'


def get_title(POSTSOUD):
    title = POSTSOUD.find(class_='title')
    if title:
        return title.text


def get_town(POSTSOUD):
    town = POSTSOUD.find(class_='title').findNext()

    if town:
        return town.tex


def get_price(POSTSOUD):
    price = POSTSOUD.find(class_='price')
    if price:
        return price.text.split()[1]


def get_number(POSTSOUD):
    number = POSTSOUD.find(class_='desc')

    if number:
        if len(number.text.strip().split()) >= 4:
            return "".join(number.text.strip().split()[1:-2])
        else:
            return ''.join(number.text.strip().split()[1:])


def get_email(POSTSOUD):
    email = POSTSOUD.find(class_='desc')

    if len(email.text.split()) >= 4 and email.text.split()[2] == 'Email:':
        return email.text.split()[-1]
    else:
        return 'no@noemail.com'

def get_descrition(POSTSOUD):
    desc = POSTSOUD.find_all(class_='desc')

    if desc:
        return desc[1].text


def run_parser_doska():
    me = User.objects.get_or_create(email='admin123@gmail.com', password='qwerty', is_superuser=True)[0]
    Category.objects.get_or_create(title='Работа')

    count_post = 0

    for q in range(200):

        link_doska = f'http://resume.doska.kg/vacancy/&page={q}&sortby=new'
        post = requests.get(link_doska, headers=headers)
        postsrc = post.text

        with open(f'adds/management/parsing/{q}.html', 'w') as file:
            file.write(postsrc)

        with open(f'adds/management/parsing/{q}.html') as file:
            postsrc = file.read()

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

            subcategory = get_subcategory(POSTSOUD)
            img = get_img(POSTSOUD)
            title = get_title(POSTSOUD)
            town = get_town(POSTSOUD)
            price = get_price(POSTSOUD)
            number = get_number(POSTSOUD)
            email = get_email(POSTSOUD)
            description = get_descrition(POSTSOUD)

            category_id = Category.objects.get(title='Работа')

            try:
                subcategory_id = Subcategory.objects.get(title=subcategory)
            except:
                Subcategory.objects.create(category=category_id, title=subcategory)
                subcategory_id = Subcategory.objects.get(title=subcategory)

            try:
                post = Post.objects.create(user=me, category=category_id, subcategory=subcategory_id,
                                    title=title,
                                    image=img,
                                    city=town, from_price=price,
                                    phone_number=number, email=email, description=description)

                post_id = Post.objects.get(pk=post.id)
                PostContacts.objects.create(post_number=post_id,
                                    phone_number=number)
                count_post += 1
            except:
                pass

            if count_post == 100:
                break

        os.remove(f'adds/management/parsing/{q}.html')

        if count_post == 100:
            break


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        time = timezone.now().strftime('%X')
        self.stdout.write("It's now %s" % time)
        run_parser_doska()
        time = timezone.now().strftime('%X')
        self.stdout.write("It's now %s" % time)
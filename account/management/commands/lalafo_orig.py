import os

import requests
from bs4 import BeautifulSoup
from django.utils import timezone
from django.core.management import BaseCommand

from account.models import UserProfile

from adds.models import Post, Category, Subcategory

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.160 YaBrowser/22.5.3.673 Yowser/2.5 Safari/537.36"
}


def get_subcategory(POSTSOUD):
    perl = POSTSOUD.find(class_='desktop css-h8ujnu').find_all('a')
    print(perl[-1].text)
    return perl[-1].text


def get_img(POSTSOUD):
    posts = POSTSOUD.find('div', class_='carousel__img-wrap').find_all('img')
    if posts:
        print("Изоб    ", 'http:' + posts[0]['src'])
        return 'http:' + posts[0]['src']


def get_title(POSTSOUD):
    title = POSTSOUD.find(class_='title')
    if title:
        print('Название   ', title.text)
        return title.text


def get_town(POSTSOUD):
    town = POSTSOUD.find(class_='title').findNext()

    if town:
        print('Город   ', town.text)
        return town.tex


def get_price(POSTSOUD):
    price = POSTSOUD.find(class_='price')
    if price:
        # print(price.text)
        return price.text.split()[1]


def get_number(POSTSOUD):
    number = POSTSOUD.find(class_='Paragraph primary')
    print("".join(number.text))



def get_email(POSTSOUD):
    email = POSTSOUD.find(class_='desc')
    if len(email.text.split()) >= 4 and email.text.split()[2] == 'Email:':
        # print('Email', email.text.split()[-1])
        return email.text.split()[-1]


def get_descrition(POSTSOUD):
    desc = POSTSOUD.find(class_='description__wrap')
    if desc:
        print(desc.text)
        return desc.text


me = UserProfile.objects.get(pk=1)
try:
    сategory_work = Category.objects.create(title='Работа')
except:
    pass




def run_pars():

    count_post = 0

    for q in range(200):

        link_doska = f'https://lalafo.kg/kyrgyzstan/rabota?sort_by=newest'
        post = requests.get(link_doska, headers=headers)
        postsrc1 = post.text

        with open(f'account/management/parsing/{q}.html','w') as file:
            file.write(postsrc1)

        with open(f'account/management/parsing/{q}.html') as file:
            postsrc = file.read()
        print('1')
        POSTSOUD = BeautifulSoup(postsrc, "lxml")
        deteil_post_links = []

        posts = POSTSOUD.find('div',class_='main-feed__container desktop css-1iavyap')
        print(posts,'---')
        break









        for k in posts:
            Iten_href1 = 'https://lalafo.kg' + k.get("href")
            deteil_post_links.append(Iten_href1)
            print(k)
        list_post_links = deteil_post_links[:-4]
        print('hi')
        for i in list_post_links:
            post = requests.get(i, headers=headers)
            postsrc = post.text
            POSTSOUD = BeautifulSoup(postsrc, "lxml")

            subcategory = get_subcategory(POSTSOUD)
            img = get_img(POSTSOUD)
            title = get_title(POSTSOUD)
            number = get_number(POSTSOUD)
            description = get_descrition(POSTSOUD)



            # town = get_town(POSTSOUD)
            # price = get_price(POSTSOUD)

            # email = get_email(POSTSOUD)


            category_id = Category.objects.get(title='Работа')

            try:
                subcategory_id = Subcategory.objects.get(title=subcategory)
            except:
                Subcategory.objects.create(category=category_id, title=subcategory)
                subcategory_id = Subcategory.objects.get(title=subcategory)

            try:
                Post.objects.create(user=me, category=category_id, subcategory=subcategory_id, title=title, image=img,
                                    phone_number=number, description=description)
                count_post += 1
            except:
                pass

            print(count_post)
            if count_post == 100:
                break

        os.remove(f'account/management/parsing/{q}.html')
        if count_post == 100:
            break




class Command(BaseCommand):
    kali = 'Sos'

    def handle(self, *args, **kwargs):
        time = timezone.now().strftime('%X')
        self.stdout.write("It's now %s" % time)
        run_pars()
        time = timezone.now().strftime('%X')
        self.stdout.write("It's now %s" % time)
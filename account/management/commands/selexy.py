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
    perl = POSTSOUD.find(class_='breadcrumb').find_all('span')
    return perl[-1].text


def get_img(POSTSOUD):
    posts = POSTSOUD.find(class_='main-content full-on-1024').find_all('img')

    if posts:
        return posts[0]['src']


def get_title(POSTSOUD):
    title = POSTSOUD.find(class_='product-name')
    if title:
        return title.text


def get_town(POSTSOUD):
    town = POSTSOUD.find(class_='column')
    if town:
        return town.tex


def get_price(POSTSOUD):
    price = POSTSOUD.find(class_='control-holder')
    if price:
        return price.text.split()[1]



def get_email(POSTSOUD):
    email = POSTSOUD.find(class_='desc')
    if len(email.text.split()) >= 4 and email.text.split()[2] == 'Email:':
        return email.text.split()[-1]


def get_descrition(POSTSOUD):
    desc = POSTSOUD.find_all(class_='description')
    if desc:
        return desc[0].text.rstrip()


me = UserProfile.objects.get(pk=1)
try:
    сategory_work = Category.objects.create(title='Работа')
except:
    pass

def run_pars_selexy():
    count_post = 0

    for q in range(1,200):

        link_doska = f'https://salexy.kg/bishkek/rabota/ishu_rabotu?page={q}'
        post = requests.get(link_doska, headers=headers)
        postsrc = post.text

        with open(f'account/management/parsing/{q}.html','w') as file:
            file.write(postsrc)

        with open(f'account/management/parsing/{q}.html') as file:
            postsrc = file.read()

        POSTSOUD = BeautifulSoup(postsrc, "lxml")
        deteil_post_links = []
        posts = POSTSOUD.find(class_="product-list").find_all("a")

        for k in posts:

            Iten_href1 =  k.get("href")
            deteil_post_links.append(Iten_href1)

        anti_copy=[]
        for i in deteil_post_links:
            if i in anti_copy:
                continue

            anti_copy.append(i)
            post = requests.get(i, headers=headers)
            postsrc = post.text
            POSTSOUD = BeautifulSoup(postsrc, "lxml")
            subcategory = get_subcategory(POSTSOUD)
            title = get_title(POSTSOUD)
            img = get_img(POSTSOUD)
            price = get_price(POSTSOUD)
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
                                    title=title, image=img,
                                    city=town, from_price=price,
                                    description=description)

                count_post += 1
            except:
                pass

            print(count_post)
            if count_post ==100:
                break

        os.remove(f'account/management/parsing/{q}.html')

        if count_post == 100:
            break



class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        time = timezone.now().strftime('%X')
        self.stdout.write("It's now %s" % time)
        run_pars_selexy()
        time = timezone.now().strftime('%X')
        self.stdout.write("It's now %s" % time)
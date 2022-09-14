from __future__ import absolute_import, unicode_literals

import os
from datetime import timedelta
from sys import stdout

import requests
from bs4 import BeautifulSoup
from celery import shared_task
from celery.task import periodic_task
from celery.schedules import crontab

from account.management.commands.catalog import run_pars_catalog
from account.management.commands.doska import *
from account.management.commands.selexy import run_pars_selexy


@periodic_task(run_every=(crontab(minute=0, hour='0,3,6,9,12,15,18,21')), name="run_selexy")
def run_selexy():
    run_pars_selexy()
    time = timezone.now().strftime('%X')
    print(time)


@periodic_task(run_every=(crontab(minute=0, hour='1,4,7,10,13,16,19,22')), name="run_cat")
def run_cat():
    run_pars_catalog()
    time = timezone.now().strftime('%X')
    print(time)


@periodic_task(run_every=(crontab(minute=0, hour='2,5,8,11,14,17,20,23')), name="run_parser")
def run_dos():
    run_parser_doska()
    time = timezone.now().strftime('%X')
    print(time)

#
# @shared_task
# def run_selex():
#
#     time = timezone.now().strftime('%X')
#     print(time)
#
# @shared_task
# def xsum(numbers):
#     return sum(numbers)

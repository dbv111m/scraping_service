import codecs
import os, sys

from django.contrib.auth import get_user_model
from django.db import DatabaseError

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ['DJANGO_SETTINGS_MODULE'] = 'scraping_service.settings'

import django
django.setup()

from scraping.myparsers import *
from scraping.models import City, Language, Vacancy, Error, Url

User = get_user_model()

parsers_ = (
    (hhru, 'https://hh.ru/search/vacancy?text=python&area=115'),
    (work, 'https://www.work.ua/ru/jobs-kyiv-python/'),
    (rabota, 'https://rabota.ua/zapros/python/%d0%ba%d0%b8%d0%b5%d0%b2/'),
    (dou, 'https://jobs.dou.ua/vacancies/?city=%D0%9A%D0%B8%D0%B5%D0%B2&category=Python'),
    (djinni, 'https://djinni.co/jobs/keyword-python/kyiv/'),
)

def get_settings ():
    qs = User.objects.filter(srnd_email = True).values()
    settings_lst = set( (q['city_id'],  q['language_id']) for q in qs)
    return settings_lst

def get_urls (_settings):
    qs = Url.objects.all().values()
    url_dict = { (q ['city_id'], q['language_id']): q['url_data']   for q in qs}
    urls = []
    for pair in _settings:
        tmp = {}
        tmp['city'] = pair[0]
        tmp['language'] = pair[1]
        tmp['url_data'] = url_dict[pair]
        urls.append(tmp)
    return urls


q = get_settings()
u = get_urls(q)

city = City.objects.filter(slug = 'kiev').first()
language = Language.objects.filter(slug = 'python').first()
jobs, errors = [], []
for parsed_site, parsed_url in parsers_:
    current_jobs, current_errors = parsed_site(parsed_url)
    jobs += current_jobs
    errors  += current_errors

for job in jobs:
    v = Vacancy(**job, city=city, language=language)
    try:
        v.save()
    except DatabaseError:
        pass

if errors:
        er = Error(data=errors).save()

# h = codecs.open('work.txt', 'w', 'utf-8')
# h.write(str(jobs))
# h.close()
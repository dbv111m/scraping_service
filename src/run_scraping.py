import codecs
import os, sys

from django.db import DatabaseError

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ['DJANGO_SETTINGS_MODULE'] = 'scraping_service.settings'

import django
django.setup()

from scraping.myparsers import *
from scraping.models import City, Language, Vacancy

parsers_ = (
    (hhru, 'https://hh.ru/search/vacancy?text=python&area=115'),
    (work, 'https://www.work.ua/ru/jobs-kyiv-python/'),
    (rabota, 'https://rabota.ua/zapros/python/%d0%ba%d0%b8%d0%b5%d0%b2/'),
    (dou, 'https://jobs.dou.ua/vacancies/?city=%D0%9A%D0%B8%D0%B5%D0%B2&category=Python'),
    (djinni, 'https://djinni.co/jobs/keyword-python/kyiv/'),
)
city = City.objects.filter(slug = 'kiev').first()
language = Language.objects.filter(slug = 'python').first()
jobs, errors = [], []
for parsed_site, parsed_url in parsers_:
    current_jobs, current_errors = parsed_site(parsed_url)
    jobs += current_jobs
    errors += current_errors

for job in jobs:
    v = Vacancy(**job, city=city, language=language)
    try:
        v.save()
    except DatabaseError:
        pass



# h = codecs.open('work.txt', 'w', 'utf-8')
# h.write(str(jobs))
# h.close()
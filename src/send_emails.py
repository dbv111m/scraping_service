import os, sys

import django
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ['DJANGO_SETTINGS_MODULE'] = 'scraping_service.settings'


django.setup()

from scraping.models import Vacancy
from scraping_service.settings import EMAIL_HOST_USER
subject = "Рассылка вакансий"
text_content = "Рассылка вакансий"
from_email = EMAIL_HOST_USER
empty = '<h2>К сожалению на сегодня по Вашим предпочтениям данных нет. </h2>'

# Получение списка емайл для рассыдки из базы https://clck.ru/T3KaK
#
User= get_user_model()
qs = User.objects.filter(srnd_email=True).values('city', 'language', 'email')

''' 
Получен список словарей <QuerySet [
{'city': 2, 'language': 1, 'email': ' m@gmail.com'}, 
{'city': 3, 'language': 1, 'email': 'u@2.ru'}, 
{'city': 1, 'language': 1, 'email': 'u@3.ru'}
]>
'''

users_dct = {}
for i in qs: # Для каждого словаря в списке qs
    users_dct.setdefault(
                        (  i['city'], i['language']),  [] )
    users_dct[(i['city'], i['language'])].append(i['email'])

if users_dct:
    params = {'city_id__in': [], 'language_id__in': []}
    for pair in users_dct.keys():
        params['city_id__in'].append(pair[0])
        params['language_id__in'].append(pair[1])
    qs = Vacancy.objects.filter(**params).values()[:10]
    vacancies = {}
    for i in qs:
        vacancies.setdefault((i['city_id'], i['language_id']), [])
        vacancies[(i['city_id'], i['language_id'])].append(i)
    for keys, emails in users_dct.items():
        rows = vacancies.get(keys, [])
        html = ''
        for row in rows:
            html += f'<h5"><a href="{ row["url"] }">{ row["title"] }</a></h5>'
            html += f'<p>{row["description"]} </p>'
            html += f'<p>{row["company"]} </p><br><hr>'
        _html = html if html else empty
        for email in emails:
            to = email
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(_html, "text/html")
            msg.send()


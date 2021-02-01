import os, sys
import datetime
import django
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ['DJANGO_SETTINGS_MODULE'] = 'scraping_service.settings'


django.setup()

from scraping.models import Vacancy
from scraping_service.settings import EMAIL_HOST_USER

today = datetime.date.today()
subject = f"Рассылка вакансий за {today}"
text_content = f"Рассылка вакансий за {today}"
from_email = EMAIL_HOST_USER
empty = '<h2>К сожалению, на сегодня по Вашим предпочтениям данных нет. </h2>'

# Получение словаря со списком емайл для рассыдки из базы данных. Визуализация: https://clck.ru/T3KaK
User= get_user_model()
qs = User.objects.filter(srnd_email=True).values('city', 'language', 'email')
users_dct = {}
for i in qs: # Для каждого словаря в списке qs
    users_dct.setdefault(
                        (  i['city'], i['language']),  [] )
    users_dct[(i['city'], i['language'])].append(i['email'])

if users_dct:
    # Формирование списка вакансий для тела письма
    params = {'city_id__in': [], 'language_id__in': []}
    for pair in users_dct.keys():
        params['city_id__in'].append(pair[0])
        params['language_id__in'].append(pair[1])
    qs = Vacancy.objects.filter(**params, timestamp=today).values()
    vacancies = {}
    for i in qs:
        vacancies.setdefault((i['city_id'], i['language_id']), [])
        vacancies[(i['city_id'], i['language_id'])].append(i)

    # Формирование и отправка писем
    for keys, emails in users_dct.items():

        # Формирование HTML для письма
        rows = vacancies.get(keys, [])
        html = ''
        for row in rows:
            html += f'<h5"><a href="{ row["url"] }">{ row["title"] }</a></h5>'
            html += f'<p>{row["description"]} </p>'
            html += f'<p>{row["company"]} </p><br><hr>'
        _html = html if html else empty

        # Отправка письма по списку
        for email in emails:
            to = email
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(_html, "text/html")
            msg.send()


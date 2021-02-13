import os, sys
import datetime
import django
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ['DJANGO_SETTINGS_MODULE'] = 'scraping_service.settings'


django.setup()

from scraping.models import Vacancy, Error, Url
from scraping_service.settings import EMAIL_HOST_USER

today = datetime.date.today()
subject = f"Рассылка вакансий за {today}"
text_content = f"Рассылка вакансий за {today}"
from_email = EMAIL_HOST_USER
ADMIN_USER = EMAIL_HOST_USER
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
        subject = f"Рассылка вакансий за {today} (ключи: {keys})"
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

# Формирование и отправка письма админу
# Начальные константы
subject = ''
text_content = ''
_html = ''

# Формирование HTML для письма админу
# 1. Ошибки скрапинга
qs = Error.objects.filter(timestamp=today)
if qs.exists():
    error = qs.first()
    data = error.data['errors']
    for i in data:
        _html += f'<p"><a href="{ i["url"] }">Error: { i["title"] }</a></p><br>'
    subject += f'Отправка ошибок за {today}'
    text_content += "Ошибки скрапинга"
    data = error.data['user_data']
    if data:
        _html += '<hr>'
        _html += '<h2>Пожелания пользователей </h2>'
        for i in data:
            _html += f'<p">Город: {i["city"]}, Специальность:{i["language"]},  Имейл:{i["email"]}</p><br>'
        subject += f" Пожелания пользователей {today}"
        text_content += "Пожелания пользователей"

# 2. Проверка наличия урлов для пар ЯП и Город
qs = Url.objects.all().values('city', 'language')
urls_dct = {(i['city'], i['language']): True for i in qs}
urls_err = ''

for keys in users_dct.keys():
    if keys not in urls_dct:
        if keys[0] and keys[1]:
            urls_err += f'<p"> Для города: {keys[0]} и ЯП: {keys[1]} отсутствуют урлы</p><br>'
if urls_err:
    subject += ' Отсутствующие урлы '
    _html += '<hr>'
    _html += '<h2>Отсутствующие урлы </h2>'
    _html += urls_err


# Отправка письма админу
if subject:
    to = ADMIN_USER
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(_html, "text/html")
    msg.send()

# Альтернативынй встроенному в Django способ отправки с использованием библиотеки smtplib
# https://docs.python.org/3/library/smtplib.html

# import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
#
# msg = MIMEMultipart('alternative')
# msg['Subject'] = 'Список вакансий за  {}'.format(today)
# msg['From'] = EMAIL_HOST_USER
# mail = smtplib.SMTP()
# mail.connect(EMAIL_HOST, 25)
# mail.ehlo()
# mail.starttls()
# mail.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
#
# html_m = "<h1>Hello world</h1>"
# part = MIMEText(html_m, 'html')
# msg.attach(part)
# mail.sendmail(EMAIL_HOST_USER, [to], msg.as_string())
# mail.quit()
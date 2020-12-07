import requests
import codecs
from bs4 import BeautifulSoup as BS
from random import randint

__all__ = ('work', 'rabota', 'dou', 'djinni')

headers_  = [
    {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:53.0) Gecko/20100101 Firefox/53.0',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
    ]


def work(url):
    jobs = []
    errors = []
    domain = 'https://www.work.ua'
    url = 'https://www.work.ua/ru/jobs-kyiv-python/'
    resp = requests.get(url, headers=headers_[randint(0, 2)])

    if resp.status_code == 200:
        soup = BS(resp.content, 'html.parser')
        main_div = soup.find('div', attrs={'id': 'pjax-job-list'})
        if main_div:
            div_lst = main_div.find_all('div', attrs={'class': 'job-link'})
            for div in div_lst:
                title = div.find('h2')
                href = title.a['href']
                content = div.p.text
                company = 'No Name'
                logo = div.find('img')
                if logo:
                    company = logo['alt']
                jobs.append({'title':title.text, 'company':company, 'url': domain+href, 'description': content})
        else:
            errors.append({'url': url, 'title': 'No Table'})

    else:
        errors.append({'url': url, 'title': 'Page is not responsing'})
    return jobs, errors


def rabota(url):
    jobs = []
    errors = []
    domain = 'https://rabota.ua'
    resp = requests.get(url, headers=headers_[randint(0, 2)])

    if resp.status_code == 200:
        soup = BS(resp.content, 'html.parser')
        new_jobs = soup.find('div', attrs='f-vacancylist-newnotfound')
        if not new_jobs:
            table = soup.find('table', attrs={'id': 'ctl00_content_vacancyList_gridList'})
            if table:
                tr_lst = table.find_all('tr', attrs={'id': True})
                for tr in tr_lst:
                    div = tr.find('div', attrs = {'class': 'card-body'})
                    if div:
                        title = div.find('h2', attrs = {'class': 'card-title'})
                        href = title.a['href']
                        content = div.find('div', attrs = {'class': 'card-description'})

                        company = 'NoName'
                        p = div.find ('p', attrs = {'class': 'company-name'})
                        if p:
                            company = p.a.text

                        jobs.append({'title':title.text, 'company': company, 'url': domain+href, 'description': content.text})
            else:
                errors.append({'url': url, 'title': 'No Div'})
        else:
            errors.append({'url': url, 'title': 'Page is empty'} )
    else:
        errors.append({'url': url, 'title': 'Page is not responsing'})
    return jobs, errors


def dou (url):
    jobs = []
    errors = []
    domain = ''
    resp = requests.get(url, headers=headers_[randint(0, 2)])

    if resp.status_code == 200:
        soup = BS(resp.content, 'html.parser')
        new_jobs = soup.find('div', attrs='f-vacancylist-newnotfound')
        if not new_jobs:
            table = soup.find('div', attrs={'id': 'vacancyListId'})
            if table:
                div_lst = table.find_all('div', attrs={'class': 'vacancy'})
                for div in div_lst:

                    div_title = div.find('div', attrs = {'class': 'title'})
                    title = div_title.text
                    href = div_title.a['href']

                    content = div.find('div', attrs = {'class': 'sh-info'})

                    company = 'NoName'
                    p = div.find ('a', attrs = {'class': 'company'})
                    if p:
                        company = p.text

                    jobs.append({'title':title, 'company': company, 'url': domain+href, 'description': content.text})

            else:
                errors.append({'url': url, 'title': 'No Div'})
        else:
            errors.append({'url': url, 'title': 'Page is empty'} )
    else:
        errors.append({'url': url, 'title': 'Page is not responsing'})
    d=1
    return jobs, errors


def djinni (url):
    jobs = []
    errors = []
    domain = 'https://djinni.co'
    resp = requests.get(url, headers=headers_[randint(0, 2)])

    if resp.status_code == 200:
        soup = BS(resp.content, 'html.parser')
        new_jobs = soup.find('div', attrs='f-vacancylist-newnotfound')
        if not new_jobs:
            table = soup.find('ul', attrs={'class': 'list-unstyled list-jobs'})
            if table:
                div_lst = table.find_all('li', attrs={'class': 'list-jobs__item'})
                for div in div_lst:

                    div_title = div.find('div', attrs = {'class': 'list-jobs__title'})
                    title = div_title.text
                    href = div_title.a['href']

                    content = div.find('div', attrs = {'class': 'list-jobs__description'})

                    company = 'NoName'
                    p = div.find ('a', attrs = {'style': 'color:#999;text-decoration:none;'})
                    if p:
                        company = p.text

                    jobs.append({'title':title, 'company': company, 'url': domain+href, 'description': content.text})

            else:
                errors.append({'url': url, 'title': 'No Div'})
        else:
            errors.append({'url': url, 'title': 'Page is empty'} )
    else:
        errors.append({'url': url, 'title': 'Page is not responsing'})
    d=1
    return jobs, errors

if __name__ == '__main__':
    url = 'https://djinni.co/jobs/keyword-python/kyiv/'
    jobs, errors = djinni(url)
    h = codecs.open('work.txt', 'w', 'utf-8')
    h.write(str(jobs))
    h.close()

import requests
import codecs
from bs4 import BeautifulSoup as BS

headers_ = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
}

domain = 'https://www.work.ua/'
url = 'https://www.work.ua/ru/jobs-kyiv-python/'
resp = requests.get(url, headers=headers_)
jobs = []
errors =[]
if resp.status_code == 200:
    soup = BS(resp.content, 'html.parser')
    main_div = soup.find('div', attrs={'id': 'pjax-job-list'})
    if main_div:
        div_lst = main_div.find_all('div', attrs={'class': 'job-link'})
        for div in div_lst:
            title = div.find('h2')
            href = title.a['href']
            name = title.a['title']
            content = div.p.text
            company = 'No Name'
            logo = div.find('img')
            if logo:
                company = logo['alt']
            jobs.append({'title':title.text, 'company':company, 'url': domain+href, 'description': content})
    else:
        errors.append({'url': url, 'title': 'No Div'})

else:
    errors.append({'url': url, 'title': 'Page is not responsing'})

h = codecs.open('work.txt', 'w', 'utf-8')
h.write(str(jobs))
h.close()
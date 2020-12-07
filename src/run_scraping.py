import codecs

from scraping.parsers import *

parsers_ = (
    (work, 'https://www.work.ua/ru/jobs-kyiv-python/'),
    (rabota, 'https://rabota.ua/zapros/python/%d0%ba%d0%b8%d0%b5%d0%b2/'),
    (dou, 'https://jobs.dou.ua/vacancies/?city=%D0%9A%D0%B8%D0%B5%D0%B2&category=Python'),
    (djinni, 'https://djinni.co/jobs/keyword-python/kyiv/'),
)

jobs, errors = [], []
for parsed_site, parsed_url in parsers_:
    current_jobs, current_errors = parsed_site(parsed_url)
    jobs += current_jobs
    errors += current_errors

h = codecs.open('work.txt', 'w', 'utf-8')
h.write(str(jobs))
h.close()
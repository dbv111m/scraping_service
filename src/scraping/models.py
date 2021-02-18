from django.db import models
# import jsonfield

from .utils import from_cyrillic_to_eng

def default_urls():
    return {'hhru': '', 'habrcom': ''}


class City(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название города',
                            unique=True)
    slug = models.CharField(max_length=50, blank=True, unique=True)

    class Meta:
        verbose_name = 'Название города'
        verbose_name_plural = 'Названия городов'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = from_cyrillic_to_eng(str(self.name))
        super().save(*args, **kwargs)


class Language(models.Model):
    name = models.CharField(max_length=50, verbose_name='Специализация',
                            unique=True)
    slug = models.CharField(max_length=50, blank=True, unique=True)

    class Meta:
        verbose_name = 'Специализация'
        verbose_name_plural = 'Специализации'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = from_cyrillic_to_eng(str(self.name))
        super().save(*args, **kwargs)

class Vacancy(models.Model):
    url = models.URLField(unique=True)
    title = models.CharField(max_length=250, verbose_name='Заголовок вакансии')
    company = models.CharField(max_length=250, verbose_name='Компания')
    description = models.TextField(verbose_name='Описание вакансии')
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name='Город')
    language = models.ForeignKey(Language, on_delete=models.CASCADE, verbose_name='Специализация')
    timestamp = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'
        ordering = ['-timestamp'] # сортировка по убыванию

    def __str__(self):
        return self.title


class Error(models.Model):
    timestamp = models.DateField(auto_now_add=True)
    data= models.JSONField()
    class Meta:
        verbose_name = 'Ошибки'
        verbose_name_plural = 'Ошибки'

    def __str__(self):
        return str(self.timestamp)

class Url(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name='Город')
    language = models.ForeignKey(Language, on_delete=models.CASCADE, verbose_name='Специализация')
    url_data = models.JSONField(default=default_urls)
    class Meta:
        unique_together = ('city', 'language')
        verbose_name = 'Пути для скрапинга'
        verbose_name_plural = 'Пути для скрапинга'
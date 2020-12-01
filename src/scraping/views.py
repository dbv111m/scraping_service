from django.shortcuts import render

from .forms import FindForm
from .models import Vacancy

# Create your views here.

def home_view(request):
    # print(request.GET) # возвращает словарь
    form = FindForm()
    city=request.GET.get('city')
    language=request.GET.get('language')
    qs=[]
    if city or language:
        _filter={}
        if city:
            _filter['city__slug'] = city # в Django обращение идет через __
        if language:
            _filter['language__slug'] = language # в Django обращение идет через __


        qs = Vacancy.objects.filter(**_filter)

    return render(request, 'scraping/home.html', {'object_list': qs, 'form': form})

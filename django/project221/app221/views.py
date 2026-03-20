from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .forms.demo_form import DemoForm

# Create your views here.
def hello(request):
    return HttpResponse("Hello, World!")

def index(request):
    template = loader.get_template("index.html")  # директорія - автоматично
    context = {               # переданий до представлення контекст
        'x': 10,              # автоматично перетворюється на змінні
        'str': 'The String'   # які можна підставляти виразами {{x}}, {{str}}
    }                         # 
    return HttpResponse( template.render(context) )


def forms(request):
    context = {            
        'get': str(request.GET),
        'x': request.GET.get('x', None),  # доступ до query-параметрів
        'demo_form': DemoForm() if request.method == 'GET' else DemoForm(request.POST),
    }                      
    return render(request, "forms.html", context)


'''
Д.З. Реалізувати окрему сторінку Intro
На ній вивести дані про встановлення та налаштування фреймворка Django
А також вивести дані про час завантаження сторіки:
 Сторінка завантажена о 14:43 13.03.2026
На головній сторінці розмістит посилання на неї
Додати скріншоти 
'''
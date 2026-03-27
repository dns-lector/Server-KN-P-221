from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .forms.demo_form import DemoForm
from .models import Client
import datetime

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
    form =  DemoForm() if request.method == 'GET' else DemoForm(request.POST)
    context = {            
        'get': str(request.GET),
        'x': request.GET.get('x', None),  # доступ до query-параметрів
        'demo_form': form,
    }
    if request.method == 'POST' :
        if form.is_valid() :
            client = Client()
            client.first_name = form.cleaned_data['first_name']
            client.last_name = form.cleaned_data['last_name']
            client.register_at = datetime.datetime.now()
            client.save()
    return render(request, "forms.html", context)


def models(request):
    context = { 
        
    }                      
    return render(request, "models.html", context)


'''
Д.З. Реалізувати на сторінці форм
виведення повідомлення про успішну реєстрацію
нового користувача.
Додати скріншоти 
'''
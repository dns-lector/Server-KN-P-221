from django.contrib import admin
from .models import *

# Register your models here.

# admin.site.register(Client) -- у такій формі модель працює, але за замовчанням

class ClientAdmin(admin.ModelAdmin) :
    list_display = ('id', 'last_name', 'first_name', 'register_at')

admin.site.register(Client, ClientAdmin) 
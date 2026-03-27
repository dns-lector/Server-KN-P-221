from django.db import models

# Create your models here.

class Client(models.Model) :
    first_name  = models.CharField(max_length=64)   # ідентифікатор можна не 
    last_name   = models.CharField(max_length=64)   # оголошувати - створиться автоматично
    register_at = models.DateTimeField()

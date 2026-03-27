from django import forms
from django.core.exceptions import ValidationError

class DemoForm(forms.Form) :
    first_name = forms.CharField(
        min_length=2, 
        max_length=64, 
        label="First name",
        error_messages={
            'required': "Ім'я необхідно зазначити",
            'min_length': "Ім'я закоротке (мін. 2 символи)",
            'max_length': "Ім'я задовге (макс. 5 символів)",
        })
    last_name = forms.CharField(min_length=2, max_length=64, label="Last name" )

    def clean(self):   # метод, що відповідає за валідацію форми
        cleaned_data = super().clean()  # запуск оброблення за замовчанням
        # якщо поле проходить валідацію, то воно потрапляє до cleaned_data
        if 'first_name' in cleaned_data :  # якщо пройдена базова валідація, додаємо власну
            first_name = cleaned_data['first_name']  # беремо за основу значення, що пройшло перевірку
            # перевіряємо, що і'мя починається з великої літери
            if not first_name[0].isupper() :
                self.add_error('first_name', ValidationError("І'мя має починатися з великої літери"))
        self.cleaned_data = cleaned_data
        return cleaned_data       

    
'''
Д.З. Забезпечити валідацію форми реєстрації (з попереднього ДЗ)
та відображення її результатів зі стилізацією
'''
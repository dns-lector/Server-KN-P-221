from django import forms

class DemoForm(forms.Form) :
    first_name = forms.CharField(min_length=2, max_length=5, label="First name")
    last_name  = forms.CharField(min_length=2, max_length=5, label="Last name" )
    
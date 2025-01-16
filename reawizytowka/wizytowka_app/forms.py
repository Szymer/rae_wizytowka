from django import forms

from wizytowka_app.models import PersonRecord






class PersonDataInput(forms.Form):
    
    name = forms.CharField(label= 'Twoje Imie i nazwisko')
    name2 = forms.DateField(label_suffix="nie wiem")
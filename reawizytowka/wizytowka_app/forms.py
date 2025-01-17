from django import forms

from wizytowka_app.models import PersonRecord






class PersonDataInput(forms.ModelForm):
    
    class Meta:
        model = PersonRecord
        fields = ("name",
                    "company_name",
                    "phone",
                    "email",
                    "photo",
                    "vcard_url",)

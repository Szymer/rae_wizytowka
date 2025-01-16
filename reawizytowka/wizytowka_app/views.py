from django.shortcuts import render
from django.views import View
from django.views.generic import FormView
from wizytowka_app.models import PersonRecord
from wizytowka_app.forms import PersonDataInput



class GetData(FormView):
    template_name = 'home.html'
    form_class = PersonDataInput
    
    def get(self, form):
          return render(self.request, self.template_name, context = {'a':"pazdzierz"})
          
        

import qrcode
from io import BytesIO
from PIL import Image, ImageDraw


from django.core.cache import cache
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import HttpResponse
from django.views.generic import FormView
from wizytowka_app.models import PersonRecord
from wizytowka_app.forms import PersonDataInput


from wizytowka_app.cermemeo_model.pydantic_models import LeadModel, Comment
from wizytowka_app.cermemeo_api import CermemeoAPI




HOST = "http://127.0.0.1:8000/"

def post_new_person(request):
    
    if request.method == 'POST':
        form = PersonDataInput(request.POST, request.FILES)
        if form.is_valid():
            person = form.save()
            # person.save()
            qr = qrcode.make(f'{HOST}person/{person.pk}', )
            frame = Image.new('RGB', (292 ,292), 'white')
            draw = ImageDraw.Draw(frame)
            frame.paste(qr, (-40, -40))
            
            filename = f'qr_{person.pk}_{person.name}png'
            buffer = BytesIO()
            frame.save(buffer, format='PNG')
            person.qr.save(filename, buffer)
            person.vcard_url = f'{HOST}person/{person.pk}'
            person.save()
            frame.close()
            pk = person.pk if person.pk else 1
            return redirect('person_detail', ipk=pk)
        else:
            context = {'form' : form}
            return render(request, 'home.html', context) 
    else:
        form = PersonDataInput()
        context  = {'form' : form}
        return render(request, 'home.html', context)
          
        
class personDetail(View):
    
    def make_qurcode(self, person):
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(f'{HOST}person/{person.pk}') 
        qr.make(fit=True)  
        qr_image = qr.make_image(fill_color='black', back_color='white')
       
        
    def get(self, request, ipk, *args, **kwargs):
        person = get_object_or_404(PersonRecord, pk=ipk)
        context = {
            'person' : person,
            'qr' : self.make_qurcode(person)
                }
        return render(request, 'person_detail.html', context)


class personList(View):

    def get(self, request):
        persons = PersonRecord.objects.all()
        context = {'traders' : persons}
        return render(request, 'traders.html', context)
    
    def post(self, request):
        pass

class leadFormView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.api = CermemeoAPI()
    
    def get(self, request, ipk , *args, **kwargs):
        trader  = get_object_or_404(PersonRecord, pk=ipk)
        context = {'trader' : trader}
        return render(request, 'lead_form.html',context)
    
    def post(self, request, ipk, *args, **kwargs):
        if request.POST.get('phone'):
            phone = request.POST.get('phone').replace(' ', '')
            trader  = get_object_or_404(PersonRecord, pk=ipk)
            try:
                lead = LeadModel(phone=phone, 
                                      campaign_token='666666')  #token zahardkodoany na produkcji podac w env
                cache.set('lead', lead, timeout = 300)
              
            except Exception as e:
                print(e)
                context = {'trader' : trader,
                            'error' : e}
                return render(request, 'lead_form.html',context)
            try:
                casched_lead = cache.get('lead')
                r =  self.api.post(casched_lead)
                print(r)
            except Exception as e:
                print(e) #dorobic obsluge bledow
            
            return redirect( 'lead_form2', ipk=ipk)
        
class leadFormViewStep2(leadFormView):
    
    def get(self, request, ipk, *args, **kwargs):
        trader  = get_object_or_404(PersonRecord, pk=ipk)
        return render(request, 'lead_forms2.html', context={'trader' : trader})
    
    def post(self, request, ipk, *args, **kwargs):
        name = request.POST.get('Name') if request.POST.get('Name') else None
        surname = request.POST.get('Surname') if request.POST.get('Surname') else None
        email = request.POST.get('email') if request.POST.get('email') else None
        comnent1 = request.POST.get('coment1') if request.POST.get('coment1') else None
        trader  = get_object_or_404(PersonRecord, pk=ipk)
        try:
            casched_lead = cache.get('lead')
            print(casched_lead)
            casched_lead.name = name
            casched_lead.surname = surname
            casched_lead.email = email
            casched_lead.comments = [Comment(text=comnent1)]
            cache.set('lead', casched_lead, timeout = 300)
        except Exception as e:
            print(e)
            context = {'error' : e}
            return render(request, 'lead_forms2.html',context)
        try:
            r =  self.api.post(casched_lead)
            print(r)
        except Exception as e:
            print(e) #dorobic obsluge bledow
        return redirect( 'lead_form3', ipk=ipk)

class leadFormViewStep3(leadFormView):
    
    def get(self, request, ipk, *args, **kwargs):
        trader  = get_object_or_404(PersonRecord, pk=ipk)
        return render(request, 'lead_forms3.html', context={'trader' : trader})
    
    def post(self, request, ipk, *args, **kwargs):
        data = request.POST.get('Data')
        miejsce = request.POST.get('Temat')
        try:
            casched_lead = cache.get('lead')
            casched_lead.comments += [Comment(text = data), Comment(text = miejsce)]
        except Exception as e:
            print(e)
            context = {'error' : e}
            return render(request, 'lead_forms3.html',context)
        try:
            r =  self.api.post(casched_lead)
            print(r)
        except Exception as e:
            print(e) #dorobic obsluge bledow
        return redirect( 'lead_forms4', ipk=ipk)


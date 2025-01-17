import qrcode
from io import BytesIO
from PIL import Image, ImageDraw


from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import HttpResponse
from django.views.generic import FormView
from wizytowka_app.models import PersonRecord
from wizytowka_app.forms import PersonDataInput



# class GetData(FormView):
#     template_name = 'home.html'
#     form_class = PersonDataInput

HOST = "http://127.0.0.1:8000/"

class personDetail(View):
    
    def make_qurcode(self, person):
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(f'{HOST}person/{person.pk}') 
        qr.make(fit=True)  
        qr_image = qr.make_image(fill_color='black', back_color='white')
        # buffer = BytesIO
        # qr_image.save(buffer, format='PNG')
        # qr_str = buffer.getvalue()
        # resp = HttpResponse(qr_image ,content_type='image/png')
        # # resp.write(qr_str)
        return qr_image
        
    
    def get(self, request, ipk, *args, **kwargs):
        try:
            person = get_object_or_404(PersonRecord, pk=ipk)
        except:
            person = PersonRecord.objects.get(pk=ipk)
        context = {
            'person' : person,
            'qr' : self.make_qurcode(person)
                }
        return render(request, 'person_detail.html', context)


def post_new_person(request):
    print(1)
    if request.method == 'POST':
        print(2)
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
          
        

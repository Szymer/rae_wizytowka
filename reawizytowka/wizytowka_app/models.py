from django.db import models



class PersonRecord(models.Model):
    name = models.CharField(max_length=127)
    company_name = models.CharField(max_length=127)
    phone = models.IntegerField()
    email = models.EmailField(unique=True)   # do przemyslenia czy napewno unique
    photo =  models.ImageField(upload_to='mediafiles/')
    qr =  models.ImageField(upload_to='mediafiles/qrcodes/', blank=True)
    vcard_url = models.URLField(default='https://ceremeo.pl/')

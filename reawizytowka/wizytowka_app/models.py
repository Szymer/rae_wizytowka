from django.db import models



class PersonRecord(models.Model):
    name = models.CharField(max_length=127)
    company_name = models.CharField(max_length=127)
    phone = models.IntegerField()
    email = models.EmailField(unique=True)   # do przemyslenia czy napewno unique
    photo =  models.ImageField()
    vard_url = models.URLField

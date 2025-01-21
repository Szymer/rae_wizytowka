"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth  import views as auth_views
from wizytowka_app.views import post_new_person, loginview, PersonDetail, PersonList, LeadFormView, LeadFormViewStep2, LeadFormViewStep3, LeadFormViewStep4, loginview, HomeView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', HomeView.as_view(), name= "home"),
    path('accounts/login/', loginview, name='login'),
    path('person/<int:ipk>/', PersonDetail.as_view(), name= "person_detail"),
    path('new_vcard/', post_new_person, name= "new_vicard"),
    path('traders/', PersonList.as_view(), name= "person_list"),
    path('contact/<int:ipk>', LeadFormView.as_view(), name= "lead_form"),
    path('contact/<int:ipk>/step2', LeadFormViewStep2.as_view(), name= "lead_form2"),
    path('contact/<int:ipk>/step3', LeadFormViewStep3.as_view(), name= "lead_form3"),
    path('contact/<int:ipk>/step4', LeadFormViewStep4.as_view(), name= "lead_form4"),
     
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
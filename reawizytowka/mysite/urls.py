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
from wizytowka_app.views import post_new_person, personDetail, personList, leadFormView, leadFormViewStep2, leadFormViewStep3

urlpatterns = [
    path('admin/', admin.site.urls),
    path('person/<int:ipk>/', personDetail.as_view(), name= "person_detail"),
    path('home/', post_new_person, name= "new_person"),
    path('traders/', personList.as_view(), name= "person_list"),
    path('contact/<int:ipk>', leadFormView.as_view(), name= "lead_form"),
    path('contact/<int:ipk>/step2', leadFormViewStep2.as_view(), name= "lead_form2"),
    path('contact/<int:ipk>/step3', leadFormViewStep3.as_view(), name= "lead_form3"),
     
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
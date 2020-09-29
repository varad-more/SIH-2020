"""sih_website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path,include    
from django.contrib.auth import views as auth_views

# from dashboard.views import index,report,rep_generatoion,register, pdf_downloader, sec_master
from dashboard.views import *
from .router import router


urlpatterns = [
    path ('admin/', admin.site.urls),
    path ('', dash_web, name ='dash_web'),
    # path ('', index, name ='index'),
    path ('future_expected', report, name='report'),
    path ('report_gen', rep_generatoion, name='report_gen'),
    path ('register',register, name ='register'),
    path ('security-master',sec_master, name ='secmaster'),
    path ('index',index , name ='index'),
    # path ('index',index , name ='index'),
    path ('pdf_downloader', pdf_downloader, name= 'pdf_downloader'),
    path ('conflict_manager', conflict_manager, name= 'conflict_manager'),
    path ('trust_ranking', trust_ranking, name= 'trust_ranking'),
    path ('login',auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path ('logout',auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path ('api/', include(router.urls)),
]

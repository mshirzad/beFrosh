from django.urls import path

from mainApp import views

app_name = 'mainApp'

urlpatterns = [
    path('', views.home, name='home'),
    path('term-condition/',
         views.term_condition, name='term-condition'),
    path('contact-us/',
         views.contact_us, name='contact-us'),
    path('about-us/',
         views.about_us, name='about-us'),
]

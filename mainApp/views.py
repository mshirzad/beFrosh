from django.shortcuts import render
from product.models import Product
from django.http import JsonResponse

import json


from django.shortcuts import render
from django.template import RequestContext




def handler404(request):
    return render(request, '404.html')



def home(request):
    products = Product.objects.all()
    
    context = {
        'products': products
    }
    return render(request, 'mainApp/index.html', context)


def term_condition(request):
    return render(request, 'mainApp/term_condition.html')


def contact_us(request):
    return render(request, 'mainApp/contact_us.html')


def about_us(request):
    return render(request, 'mainApp/about_us.html')

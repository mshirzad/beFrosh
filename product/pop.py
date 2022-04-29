import os
import django
from product.models import Product
from faker import Faker



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'beFrosh.settings')
django.setup()

fakegen=Faker()

def pop(n=50):

    for ent in range(50):
        
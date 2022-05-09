import os
import uuid

from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import User

# from product.models import Product

def image_path_generator(instance, filename):
    extension = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{extension}'

    return os.path.join(f'sellers/', filename)

class Location (models.Model):
    country = models.CharField(max_length=128)
    province = models.CharField(max_length=128)
    district = models.CharField(max_length=128)
    region = models.CharField(max_length=128)
    street = models.CharField(max_length=128)
    address_line = models.CharField(max_length=128)

    def __str__(self) -> str:
        addr = f'{self.address_line} {self.street} {self.region} {self.province}'
        return addr


class Seller (models.Model):
    photo = models.ImageField(null=True, upload_to=image_path_generator, blank=True)
    phone_no = models.IntegerField()
    whatsapp_no = models.IntegerField(null=True)
    rating = models.FloatField()
    user_name = models.OneToOneField(
        User, related_name='seller', on_delete=models.CASCADE)
    address = models.ForeignKey(
        Location, related_name='seller', on_delete=CASCADE)
    def __str__(self) -> str:
        return f'{self.user_name.first_name} {self.user_name.last_name}'

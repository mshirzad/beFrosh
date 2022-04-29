import uuid

from django.db import models
from django.db.models.deletion import CASCADE
from seller.models import Seller
from django.utils import timezone


class Product (models.Model):
    p_pk = models.UUIDField(primary_key=True, default=uuid.uuid4)
    title = models.CharField(null=False, max_length=128)
    desc = models.CharField(null=False, max_length=512)
    price = models.FloatField()
    catagory = models.CharField(max_length=128)
    sold_status = models.BooleanField(default=False)
    image = models.ImageField(
        upload_to='product-images', blank=True, null=True)
    seller = models.ForeignKey(
        Seller, related_name='product', on_delete=CASCADE)

    total_rating = models.FloatField(default=0)
    no_rating = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.title

    def product_add(self):
        add = self.seller.address
        return f'{add.country} {add.province} {add.district} {add.street} {add.region} {add.address_line}'


class FaveProduct(models.Model):
    p_pk = models.UUIDField(primary_key=True, default=uuid.uuid4)
    product = models.ForeignKey(
        Product, related_name='product', on_delete=CASCADE)
    faver = models.ForeignKey(
        Seller, related_name='faver', on_delete=CASCADE)

    def __str__(self):
        return f'{self.product.title} is Loved By {self.faver.user_name.username}'


class ProdComment(models.Model):
    p_pk = models.UUIDField(primary_key=True, default=uuid.uuid4)
    text = models.CharField(null=False, max_length=128)
    product = models.ForeignKey(
        Product, related_name='commentproduct', on_delete=CASCADE)
    commenter = models.ForeignKey(
        Seller, related_name='commentor', on_delete=CASCADE)
    pub_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.text} is Loved By {self.commenter.user_name.username}'

    def pretty_date(self):
        date = self.pub_date
        # return f'{date.strftime("%d %B, %Y %-I:%M:%S %p")}'
        return f'{date.strftime("%d %B, %Y")}'


class Rating (models.Model):
    p_pk = models.UUIDField(primary_key=True, default=uuid.uuid4)
    rater = models.ForeignKey(
        Seller, related_name='seller_rating', on_delete=CASCADE)
    rated = models.ForeignKey(
        Product, related_name='product_rating', on_delete=CASCADE)
    value = models.IntegerField(default=0)

    def __str__(self) :
        return str(self.value) + ' by ' + self.rater.user_name.username

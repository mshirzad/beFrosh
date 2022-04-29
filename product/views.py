import io
import json

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from rest_framework.parsers import JSONParser

from product.models import Product, FaveProduct, ProdComment, Rating
from seller.models import Seller

from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder


@login_required(login_url='/seller/become-seller/')
def productDetails(request, prod_pk):

    product = Product.objects.get(pk=prod_pk)
    comments = ProdComment.objects.filter(
        product=product).order_by('-pub_date')
    context = {'product': product, 'comments': comments}

    return render(request, 'product/product_details.html', context)


@login_required(login_url='/seller/become-seller/')
def addProduct(request):

    user = request.user

    if request.method == 'GET':

        try:
            Seller.objects.get(user_name=user)
            return render(request, 'product/add_new.html')
        except Seller.DoesNotExist:
            return redirect('seller:become-seller')

    elif request.method == 'POST':
        data = request.POST
        is_seller = True

        try:
            seller_ = Seller.objects.get(user_name=user)
        except Seller.DoesNotExist:
            is_seller = False

        for key in data:
            if data[key] == '':

                resp = {'error': True,
                        'message': f'{key} Can\'t Be Empty', 'error-key': key}
                return JsonResponse(resp)

        if is_seller:
            try:
                product_ = Product.objects.create(
                    title=data['title'], desc=data['desc'],
                    price=data['price'], catagory=data['catagory'],
                    image=request.FILES.get('product-pic'),
                    seller=user.seller)
                product_.save()

            except Exception as e:
                resp = {'error': True, 'message': 'PRODUCT NOT ADDEDD'}
                return JsonResponse(resp)
        else:
            resp = {
                'error': True, 'message': 'You must create Seller account before lisitng product'}
            return JsonResponse(resp)

        resp = {'error': False,
                'message': 'PRODUCT ADDEDD SUCCESSFULLY', "success_url": '/'}

        return JsonResponse(resp)


@login_required(login_url='/seller/become-seller/')
def add_fav(request):
    success_url = 'http://127.0.0.1:8000/seller/become-seller/'

    if request.user.is_authenticated:
        product_id = json.loads(request.body).get('product_id')
        product = Product.objects.get(pk=product_id)
        is_faver = True

        try:
            faver = Seller.objects.get(user_name=request.user)
        except Seller.DoesNotExist:
            is_faver = False
            return JsonResponse({'error': True, 'message': 'Create seller account First', 'success_url': success_url})

        if is_faver:
            try:
                FaveProduct.objects.get(product=product, faver=faver)
                return JsonResponse({'error': True, 'message': 'Already in favorites'})

            except FaveProduct.DoesNotExist:
                fave_product = FaveProduct.objects.create(
                    product=product, faver=faver)
                fave_product.save()
                return JsonResponse({'error': False, 'message': 'Added to Favorites'})

    return JsonResponse({'error': True, 'message': 'Something went wrong'})


def favorites(request):
    user = request.user
    is_seller = True

    try:
        current_seller = Seller.objects.get(user_name=user)
    except Seller.DoesNotExist:
        is_seller = False
        return redirect('seller:become-seller')

    if is_seller:

        products = Product.objects.filter(seller=current_seller)
        faves = FaveProduct.objects.filter(faver=current_seller)
        context = {'my_listings_len': len(
            products), 'favorites_len': len(faves),
            'products': faves}

        return render(request, 'product/fave.html', context)


def my_listings(request):
    user = request.user
    is_seller = True

    try:
        seller_ = Seller.objects.get(user_name=user)
    except Seller.DoesNotExist:
        is_seller = False
        return redirect('seller:become-seller')

    if is_seller:
        products = Product.objects.filter(seller=seller_)
        faves = FaveProduct.objects.filter(faver=seller_)

        context = {'my_listings_len': len(
            products), 'favorites_len': len(faves),
            'products': products}

        # products = serializers.serialize('json', products_set)
        return render(request, 'product/my_listings.html', context)
        # return JsonResponse({'products': products})


def search_products(request):
    data = json.loads(request.body)
    search_text = data.get('search_text')
    catagory = data.get('catagory')
    location = data.get('search_location')
    rating = data.get('top-rating')
    low_price = data.get('lowest-price')
    high_price = data.get('high-price')

    products_set = {}
    products = []

    if data.get('empty'):
        products_set = Product.objects.all()

    if rating:
        products_set = Product.objects.filter(
            Q(total_rating__gte=3.5) &
            Q(sold_status=False))

    if low_price:
        products_set = Product.objects.filter(
            Q(price__lte=200) &
            Q(sold_status=False))

    if high_price:
        products_set = Product.objects.filter(
            Q(price__gte=1000) &
            Q(sold_status=False))

    if search_text and len(search_text):
        products_set = Product.objects.filter(
            Q(title__contains=search_text) |
            Q(desc__contains=search_text) |
            Q(price__contains=search_text) |
            Q(catagory__contains=search_text) &
            Q(sold_status=False))

    if catagory:
        products_set = Product.objects.filter(
            Q(catagory=catagory) &
            Q(sold_status=False))

    if location:
        products_set = Product.objects.filter(
            Q(product_add__contains=location) &
            Q(sold_status=False))

    for product in products_set:
        products.append({
            'fields': {
                'title': product.title,
                'address': product.product_add(),
                'desc': product.desc,
                'catagory': product.catagory,
                'price': product.price,
                'seller': product.seller.user_name.get_full_name(),
                'image': product.image.name,
                'total_rating': product.total_rating,
                'no_rating': product.no_rating,

            },
            'pk': product.pk
        })

    return JsonResponse(products, safe=False)


def add_comment(request):

    data = json.loads(request.body)
    product_id = data.get('product-id')
    text = data.get('text')
    rating_val = int(data.get('rating'))/20

    if request.user.is_authenticated:

        try:
            product = Product.objects.get(p_pk=product_id)
            seller = Seller.objects.get(user_name=request.user)
        except Seller.DoesNotExist or Product.DoesNotExist:
            return JsonResponse({'error': True, 'message': 'You are not a seller'})

        comment = ProdComment.objects.create(
            text=text, product=product,
            commenter=seller)

        if len(text) == 0:
            return JsonResponse({'error': True,
                                 'message': 'Comment can not be empty text'})
        else:
            comment.save()

        rating, is_created = Rating.objects.update_or_create(
            rater=seller, rated=product, value=rating_val)

        if is_created:
            product.total_rating = product.total_rating + rating_val
            product.no_rating = product.no_rating+1
        else:
            product.total_rating = product.total_rating-rating_value
            print(rating.value)
            product.total_rating = product.total_rating + rating_val
        product.save()

        return JsonResponse({'error': False, 'message': 'Rated and commented successfully'})

    else:
        return JsonResponse({'error': True, 'message': 'Login First'})


def delete_item(request):
    user = request.user
    if user.is_authenticated:
        product_id = json.loads(request.body)['product_id']
        product = Product.objects.get(p_pk=product_id)
        seller = Seller.objects.get(product=product)

        if user.id == seller.user_name.id:
            product.delete()
            return JsonResponse({'error': False, 'message': 'Successfully Deleted'})
        else:
            return JsonResponse({'error': True, 'message': 'Permission Denied'})
    return JsonResponse({'error': False, 'message': 'Login First'})


def delete_fave(request):
    user = request.user
    if user.is_authenticated:

        product_id = json.loads(request.body)['product_id']
        product = Product.objects.get(p_pk=product_id)
        seller = Seller.objects.get(user_name=user)
        fave_prod = FaveProduct.objects.filter(product=product, faver=seller)
        fave_prod.delete()
        return JsonResponse({'error': False, 'message': 'Successfully Deleted'})

    return JsonResponse({'error': False, 'message': 'Login First'})
    # return redirect('seller:register')

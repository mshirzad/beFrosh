import imp
import io
import json
import os
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from rest_framework.parsers import JSONParser

from seller.models import Seller, Location
from product.models import Product, FaveProduct
from beFrosh.settings import DOMAIN


@login_required(login_url='/seller/login/')
def logout_(request):
    logout(request)
    return HttpResponseRedirect('/seller/login/')


def loginView(request):
    success_url = f'{DOMAIN}/seller/become-seller/'

    if request.user.is_authenticated:
        return redirect('seller:become-seller')

    if request.method == 'GET':
        return render(request, 'seller/login.html')

    elif request.method == 'POST':
        data = json.loads(request.body)

        for key in data:
            if data[key] == '' and key != 'next':

                resp = {'error': True,
                        'message': f'{key} Can not Be Empty', 'error-key': key}
                return JsonResponse(resp)

        username = data['username']
        password = data['password']

        msg = ''

        if not request.user.is_authenticated:
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                nexturl = data.get('next')
                success_url = f'{DOMAIN}/'+nexturl

                resp = {'error': False, 'message': "LOGIN SUCCESSFULL",
                        'success_url': '/'}

                return JsonResponse(resp)

            else:
                msg = 'Username or Password is Incorrect!'
                resp = {'error': True, 'message': msg}
                return JsonResponse(resp)

        else:
            resp = {'error': False,
                    'success_url': success_url}
            return JsonResponse(resp)


@login_required(login_url='/seller/login/')
def changePassword(request):
    success_url = f'{DOMAIN}/seller/become-seller/'

    if request.method == 'GET':
        return render(request, 'seller/changepass.html')

    if request.method == 'POST':
        data = json.loads(request.body)
        user = request.user

        for key in data:
            if data[key] == '':

                resp = {'error': True,
                        'message': f'{key} Can not Be Empty', 'error-key': key}
                return JsonResponse(resp)

        current_password = data['current_password']
        new_password = data['new_password']
        confirm_password = data['confirm_password']

        if user.check_password(current_password):

            if confirm_password != new_password:
                resp = {'error': True, 'message': "Password didn't Match"}
                return JsonResponse(resp)

            else:
                user.set_password(new_password)
                user.save()
                resp = {'error': False, 'message': "Password Changed",
                        "success_url": success_url}
                return JsonResponse(resp)

        else:
            resp = {'error': True, 'message':  "Your Current Incorrect Password"}
            return JsonResponse(resp)


@login_required(login_url='/seller/login/')
def becomeSeller(request):

    if request.method == 'GET':
        try:

            seller = Seller.objects.get(user_name=request.user)
            products = Product.objects.filter(seller=seller)
            faves = FaveProduct.objects.filter(faver=seller)
            context = {"seller": seller, 'my_listings_len': len(
            products), 'favorites_len': len(faves)}
            return render(request, 'seller/profile.html', context)
        except Seller.DoesNotExist:
            return render(request, 'seller/profile.html')

    elif request.method == 'POST':
        data = json.loads(request.body)
        for key in data:
            if data[key] == '':

                resp = {'error': True,
                        'message': f'{key} Can not Be Empty', 'error-key': key}
                return JsonResponse(resp)

        try:
            location_defaults = {
                'country': data['country'],
                'province': data['province'],
                'region': data['region'],
            }

            location, l_created = Location.objects.update_or_create(
                seller__user_name=request.user, defaults=location_defaults)

        except Exception as e:
            return JsonResponse({'error': True, "message": 'Unable to add location'})

        try:
            user = request.user
            user.first_name = data['first_name']
            user.last_name = data['last_name']
            user.email = data['email']
            user.save()
            seller, s_created = Seller.objects.update_or_create(
                phone_no=data['phone_no'],
                whatsapp_no=data['whatsapp_no'],
                rating=0,
                address=location,
                user_name=request.user)
        except Exception as e:
            return JsonResponse({'error': True, "message": 'Unable to add seller'})

        return JsonResponse({'error': False, "message": 'Status Updated Successfully', 'success_url': '/'})


def change_usrpic(request):
    if request.method == 'POST':
        user = request.user
        is_seller = True

        try:
            seller_ = Seller.objects.get(user_name=user)
        except Seller.DoesNotExist:
            is_seller = False

        if is_seller:
            usrpic = request.FILES.get('usrpic')
            file_ext = os.path.splitext(str(request.FILES.get('usrpic')))[1]
            supported_ext = ['.png', '.jpg', '.jpeg']

            if file_ext.lower() in supported_ext and usrpic is not None:

                seller = Seller.objects.get(user_name=request.user)
                seller.photo = usrpic
                seller.save()
                return JsonResponse({'is_updated': True})
            else:
                JsonResponse({"is_updated": False})
        else:
            return JsonResponse({'error': True, 'message': 'To add/change profile photo you have to become seller first'})

    return JsonResponse({"is_updated": False})


def register(request):

    if request.method == 'GET':
        if request.user.is_authenticated:
            logout(request)
        return render(request, 'seller/signup.html')

    elif request.method == 'POST':
        data = json.loads(request.body)
        print(data)
        for key in data:  # IF ANY OF DATA IS EMPTY
            if data[key] == '':
                resp = {'error-key': key, 'error': True,
                        'message': f'Empty {key} is not allowed'}
                return JsonResponse(resp)

        if data['password'] != data['r_password']:
            resp = {'error': True, 'message': 'Password didn\'t Match'}
            return JsonResponse(resp)

        f_name = data['first_name']
        l_name = data['last_name']

        try:
            user = User.objects.create_user(
                data['username'], data['email'], data['password'], first_name=f_name, last_name=l_name)
            login(request, user)
            resp = {'error': False,
                    'message': 'USER CREATED SUCCESFULLY', "success_url": '/'}

            return JsonResponse(resp)

        except Exception as e:
            resp = {'error': True, 'message': 'Username already exists'}
            return JsonResponse(resp)

        # user.save()

        # resp = {'error': False,
        #         'message': 'USER CREATED SUCCESFULLY', "success_url": '/'}
        # return JsonResponse(resp)


def delete_account(request):
    if request.user.is_authenticated:
        user = request.user
        seller = Seller.objects.get(user_name=user)
        user.delete()
        seller.delete()
    return redirect('seller:register')

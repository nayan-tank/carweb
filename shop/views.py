from django.shortcuts import render
from .forms import *
from django.contrib import messages
from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.core.paginator import Paginator
from carweb import urls 
from .models import *
from itertools import chain
from django.contrib.auth.models import User
import smtplib as s
import random
import requests
import http.client
from django.conf import settings
from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from instamojo_wrapper import Instamojo

from dotenv import load_dotenv
import os
load_dotenv()  


BASE_URL = 'http://127.0.0.1:8000'

#instamojo payment 

#api is variable name 
api=Instamojo(api_key=settings.API_KEY, auth_token=settings.AUTH_TOKEN ,endpoint="https://test.instamojo.com/api/1.1/" )


# verify_otp
def verify_otp(request):
    pass

# Car Order 
def car_order(request,id):
    if request.user.is_authenticated:
        try:
            car_obj=Car.objects.get(pk=id)#uid 5:09
            order_obj , _ = Order.objects.get_or_create(
                car_id=car_obj,
                user_id=request.user,
                is_paid=False
            )
            
            print('order: ', order_obj)
            response=api.payment_request_create(
                amount='1000',
                # amount=order_obj.car_id.price,
                purpose=f'Advance booking of {car_obj.car_name}',
                buyer_name=f'{request.user.first_name}',
                email=request.user.email,
                # allow_repeated_payments=False,
                phone='9687214281',
                # send_sms=True,
                redirect_url=f'{BASE_URL}/order-success/'
            )

            print('response: ' ,response)
            order_obj.order_id=response['payment_request']['id']
            order_obj.amount=response['payment_request']['amount']
            order_obj.instamojo_response=response
            order_obj.save() 

            url = response['payment_request']['longurl']
            # url = 'https://test.instamojo.com/@achieversacademy0108/ldb7f0b9991dd4fe8b3b61fd73851cf06/'

            return redirect(url)

        except Exception as e:
            print(e)
    else:
        return redirect('login')

    return redirect('home')



# Order Success
def order_success(request):
    if request.user.is_authenticated:
        payment_request_id = request.GET.get('payment_request_id')
        if payment_request_id != None:
            order_obj=Order.objects.get(order_id=payment_request_id)
            order_obj.is_paid = True
            order_obj.status = 'SUCCESS'


            car = Car.objects.get(pk=order_obj.car_id.car_id)
            car.sold_out = 1
            car.save()

            order_obj.save()

            return render(request, 'payment/success.html') 
        else:
            return redirect('home')
    else:
        return redirect('login')


# User Registration 
def user_signup(request):
    if request.method == 'POST':
        # print(request.FILES)
        fm = SignUpForm(request.POST, request.FILES)
       
        if fm.is_valid():
            fm.save()
            uname = fm.cleaned_data['username']
            password = fm.cleaned_data['password1']

            user = authenticate(username=uname, password=password)
            
            if user is not None:

                login(request, user)
                # send welcome email
                obj = s.SMTP('smtp.gmail.com', 587)
                obj.ehlo()
                obj.starttls()
                obj.login(str(os.getenv('EMAIL_USER')), str(os.getenv('EMAIL_PASSWORD')))
                SUBJECT = f'Hey {request.user}'
                BODY = f'Thank you for register in our app. i hope you will get best deal. Have a nice day...'
                message = "subject: {} \n\n{}".format(SUBJECT, BODY)
                TO = [ fm.cleaned_data['email'] ]

                obj.sendmail(str(os.getenv('EMAIL_USER')), TO, message)

                print('send mail success')

                obj.quit()
                
                phone = fm.cleaned_data['phone']
                user = User.objects.get(pk=request.user.id)
                profile = Profile()
                profile.user = user
                profile.phone = phone
                profile.otp = random.randint(1000, 9999) 
                profile.save()

                return redirect('home')
        else:
            print('error')
    else:
        fm = SignUpForm()
    return render(request, 'accounts/signup.html', {'fm': fm})


def success(request):
    return render(request, 'payment/success.html')


# User Login 
def user_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            fm = AuthenticationForm(request=request, data=request.POST)
            if fm.is_valid():
                uname = fm.cleaned_data['username']
                password = fm.cleaned_data['password']
                user = authenticate(username=uname, password=password)
                if user is not None:
                    login(request, user)

                    return redirect('home')
        else:
            fm = AuthenticationForm()
    else:
        return redirect('dashboard')
    return render(request, 'accounts/login.html', {'fm':fm})



# change password
# @login_required
def changepass(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            fm = SetPasswordForm(user=request.user, data=request.POST) 
            if fm.is_valid():
                fm.save()
                messages.success(request, 'Your password has been changed successfully !')
                update_session_auth_hash(request, fm.user)
                return redirect('home')
        else:
            fm = SetPasswordForm(user=request.user) 
        return render(request, 'accounts/changepass.html', {'fm': fm})   
    else:
        return redirect('login')

# Password reset form 
def resetpass(request):
    fm = PasswordChangeForm(request)
    return render(request, 'accounts/changepass.html', {'fm': fm})


# User Logout
def user_logout(request):
    logout(request)
    return redirect('login')


# Orders
def order(request):
    if request.user.is_authenticated:
        user_id = request.user.id

        # sell
        user_sell = CarRequest.objects.filter(user_id=user_id).order_by('-car_request_id')

        # buy
        # data = CompanySell.objects.filter(user_id=user_id)
        # user_buy = Car.objects.filter(car_id__in=data.values('car_id'))

        data = Order.objects.filter(user_id = user_id)
        user_buy = Car.objects.filter(car_id__in=data.values('car_id')).order_by('-purc_date')

        # print(user_buy)

        sell_img = RequestCarImage.objects.filter(car_req_id__in=user_sell.values('car_request_id'))


        print(sell_img)
        # print(cars.query)

        context = {
            'user_buy' : user_buy,
            'user_sell' : user_sell,
            'sell_img': sell_img,
            # 'buy_img': buy_img
        }

        # print(context)
        
        return render(request, 'accounts/order.html', context)
    else:
        return redirect('login')


# Dashboard
def dashboard(request):
    if request.user.is_authenticated:

        if request.user.is_superuser:
            return redirect('/admin')

        if request.GET.get('verify'):
            # print('verify clicked')
            otp = request.GET.get('otp')
            user = Profile.objects.get(user=request.user)

            if otp == user.otp:
                messages.success(request, 'Email verified successfully...!')
                user.is_verified = True
                user.save()
                return redirect('dashboard')
            else:
                messages.warning(request, 'Invalid OTP !!')
                return redirect('dashboard')


        if request.GET.get('send_otp'):
            # print('send otp clicked')
            user = Profile.objects.get(user=request.user)
            user.otp = random.randint(1000, 9999)
            user.save()

            obj = s.SMTP('smtp.gmail.com', 587)
            obj.ehlo()
            obj.starttls()
            obj.login(str(os.getenv('EMAIL_USER')), str(os.getenv('EMAIL_PASSWORD')))
            SUBJECT = f'OTP Verification'
            BODY = f'Your OTP is {user.otp}'
            message = "subject: {} \n\n{}".format(SUBJECT, BODY)
            TO = [ request.user.email ]
            obj.sendmail(str(os.getenv('EMAIL_USER')), TO, message)
            # print('send mail success')
            obj.quit()

            messages.success(request, 'OTP sent to your email address ...')
            return redirect('dashboard')                        


        if request.method == 'POST':
            user_form = UpdateUserForm(request.POST, instance=request.user)
            # pic = request.FILES.get('file')
            profile = Profile.objects.get(user=request.user)


            if request.FILES.get('file'):
                print('file')
                profile.avatar = request.FILES.get('file')
                # profile.save()


            if request.POST.get('phone'):
                print('phone')
                # profile = Profile.objects.get(user=request.user)
                profile.phone = request.POST.get('phone')
                profile.save()


            if user_form.is_valid():
                email = user_form.cleaned_data['email']
                
                try:
                    match = User.objects.get(email__iexact=email)
                except User.DoesNotExist:
                    # user_form.save()
                    messages.success(request, 'Your profile updated successfully')
                else:
                    if match.id == request.user.id:
                        messages.success(request, 'Your profile updated successfully')
                        user_form.save()
                    else:
                        messages.warning(request, 'Opps..! This email already in used')
            
                return redirect(to='dashboard')
            else:
                messages.warning(request, 'Opps..! enter valid data')
        else:
            user_form = UpdateUserForm(instance=request.user)
            profile = Profile.objects.get(user=request.user)

        context = {
                'user_form': user_form,
                'profile': profile
            }

        return render(request, 'accounts/profile.html', context)
    else:
        return redirect('login')

    

# User Car Request
def car_request(request):
    if request.user.is_authenticated:
        # user = User.objects.get(pk=request.user.id)
        profile = Profile.objects.get(user=request.user)
        if not profile.is_verified and not request.user.is_superuser:
            messages.warning(request, 'Kindly, verify your email first!!')
            return redirect('dashboard')

        if request.method == 'POST':
            fm = UserRequest(request.POST, request.FILES)

            # print(fm)
            if fm.is_valid(): 
                instance = fm.save(commit=False)
                instance.user_id = request.user
                # print(instance)

                car_name = fm.cleaned_data['car_name']
                print(car_name)

                instance.save()
                # print(request.user.id)
                
                car_req_id = CarRequest.objects.filter(user_id=request.user.id).first()
                
                for each in request.FILES.getlist('images'):
                    img = RequestCarImage(image_path=each, car_req_id=car_req_id,)
                    img.save()


                messages.success(request, f'Thanks {request.user}. We got your request, our team will rich you soon...')
                return redirect('home')
        else:
            fm = UserRequest()
    else:
        return redirect('login')
    return render(request, 'request.html', {'fm': fm})



# Complain 
def complain(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            fm = UserComplain(request.POST)
            if fm.is_valid():
                instance = fm.save(commit=False)
                instance.user_id = request.user
                instance.save()
                messages.success(request, f'Sorry for inconvenient {request.user}. We solve your problem soon.')
                return redirect('home')
        else:
            fm = UserComplain()
    else:
        return redirect('login')
    return render(request, 'complain.html', {'fm': fm})



# Inquiry
# def inquiry(request):
#     if request.user.is_authenticated:
#         if request.method == 'POST':
#             fm = UserInquiry(request.POST)
#             if fm.is_valid():
#                 instance = fm.save(commit=False)
#                 instance.user_id = request.user
#                 instance.save()
#                 messages.success(request, 'We have got your query. we will connect you soon ...')
#                 return redirect('home')
#         else:
#             fm = UserInquiry()
#     else:
#         return redirect('login')
#     return render(request, 'inquiry.html', {'fm': fm})


# Car details page
def cardetails(request, id):
    if request.user.is_authenticated:
        try:    
            car = Car.objects.get(pk=id)
        except Car.DoesNotExist: 
            return redirect('/')  
                
        # if car.sold_out == 0:

        brand_id = car.model_id.brand_id

        models = Model.objects.all().filter(brand_id=brand_id)
        related_cars = Car.objects.filter(model_id__in=models.values('model_id'), sold_out=0).exclude(pk=id)

        context = {'car': car, 'related': related_cars,}

        return render(request, 'test.html', context)
        # else:
        #     return redirect('home')
    else:
        return redirect('login')




# Review
def review(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            fm = UserFeedback(request.POST) 
            if fm.is_valid():
                instance = fm.save(commit=False)
                instance.user_id = request.user
                instance.save()
                messages.success(request, f'Thank you for your valuable time {request.user} !')
                return redirect('home')
        else:
            fm = UserFeedback()
    else:
        return redirect('login')
    return render(request, 'review.html', {'fm': fm})


# Gallery
def gallery(request, cid):
    if request.user.is_authenticated:
        try:
            cars = Image.objects.filter(car_id=cid)
            carname = Car.objects.get(pk=cid)
            print(carname)
            return render(request, 'gallery.html', {'cars': cars, 'carname': carname})
        except Car.DoesNotExist: 
            return HttpResponse('Exception: Data Not Found')
    else:
        return redirect('home')


# About us 
def about_us(request):
    return render(request, 'about.html')


# Error Page
def error_404_view(request, exception):
    return render(request, '_404.html')



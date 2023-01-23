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


# User Registration 
def user_signup(request):
    if request.method == 'POST':
        fm = SignUpForm(request.POST)
       
        if fm.is_valid():
            fm.save()
            uname = fm.cleaned_data['username']
            password = fm.cleaned_data['password1']
            user = authenticate(username=uname, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
        else:
            print('error')
    else:
        fm = SignUpForm()
    return render(request, 'accounts/signup.html', {'fm': fm})


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
                    return redirect('dashboard')
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
                messages.success(request, 'Password change successfully...')
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



# Dashboard
def dashboard(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)

        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='dashboard')
    else:
        user_form = UpdateUserForm(instance=request.user)


    if request.user.is_authenticated:
        user_id = request.user.id
        # buy
        user_sell = CarRequest.objects.filter(user_id=user_id)

        # sell
        # user = User.objects.get(pk=user_id)
        car_sell = CompanySell.objects.filter(user_id=user_id)
        cars = Car.objects.filter(car_id__in=car_sell.values('car_id'))

        sell_img = Image.objects.filter(car_req_id__in=user_sell.values('car_request_id'))
        # buy_img = Image.objects.filter(car_id=)
        

        # print(cars.query)

        context = {
            'user_buy' : cars,
            'user_sell' : user_sell,
            'user_form': user_form,
            'sell_img': sell_img,
            # 'buy_img': buy_img
        }

        return render(request, 'accounts/profile.html', context)
    else:
        return redirect('login')



# User Car Request
def car_request(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            fm = UserRequest(request.POST, request.FILES)

            # print(fm)
            if fm.is_valid(): 
                instance = fm.save(commit=False)
                instance.user_id = request.user
                # print(instance)
                instance.save()
                # print(request.user.id)

                car_req_id = CarRequest.objects.filter(user_id=request.user.id).first()
                

                for each in request.FILES.getlist('images'):
                    img = Image(image_path=each, car_req_id=car_req_id,)
                    img.save()

                messages.success(request, 'Request send successfully...')
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
                messages.success(request, 'Complain send successfully...')
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
            return HttpResponse('Exception: Data Not Found')    
        
        if car.sold_out == 0:

            brand_id = car.model_id.brand_id

            models = Model.objects.all().filter(brand_id=brand_id)
            related_cars = Car.objects.filter(model_id__in=models.values('model_id'), sold_out=0).exclude(pk=id)

            # print(car.model_id.brand_id)
            # print(related_cars)

            return render(request, 'test.html', {'car': car, 'related': related_cars})
        else:
            return redirect('home')
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
                messages.success(request, 'Thank you for your valuable time !')
                return redirect('home')
        else:
            fm = UserFeedback()
    else:
        return redirect('login')
    return render(request, 'review.html', {'fm': fm})


# Gallery
def gallery(request, cid):
    try:
        cars = Image.objects.filter(car_id=cid)
        carname = Car.objects.get(pk=cid)
        print(carname)
        return render(request, 'gallery.html', {'cars': cars, 'carname': carname})
    except Car.DoesNotExist: 
        return HttpResponse('Exception: Data Not Found')

 
# Payment
def payment(request):
    pass



# Error Page
def error_404_view(request, exception):
    return render(request, '_404.html')


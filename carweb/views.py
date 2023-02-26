from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.contrib import messages
from shop.models import *
from shop.forms import *
from shop.helpers import *
from datetime import datetime

# from django.db.models import Q
import io
from django.http import FileResponse
from django.template.loader import get_template
import xhtml2pdf.pisa as pisa
from django.template.loader import render_to_string

# home 
def home(request):
    # get request for car
    # cars = Car.objects.filter(sold_out=0)
    cars = Car.objects.all()
    reviews = Review.objects.all()
    brands = Brand.objects.all()
    # print(reviews)

    # sorting
    if request.GET.get('sort') == 'ATZ':
        cars = Car.objects.all().order_by('car_name').values()

    if request.GET.get('sort') == 'ZTA':
        cars = Car.objects.all().order_by('-car_name').values()

    if request.GET.get('sort') == "LTH":
        cars = Car.objects.all().order_by('price').values()

    if request.GET.get('sort') == "HTL":
        cars = Car.objects.all().order_by('-price').values()
    
    if request.GET.get('sort') == "latest":
        cars = Car.objects.all().order_by('-purc_date').values()


    # #########  filter  #########

    # by color
    if request.GET.get('color'):
        color = request.GET.get('color')
        cars = Car.objects.filter(color__icontains=color)

    # by fuel
    if request.GET.get('fuel'):
        fuel = request.GET.get('fuel')
        cars = Car.objects.filter(fuel_type__icontains=fuel)
        # print(cars)

    # by brand
    if request.GET.get('brand'):
        brand_id = request.GET.get('brand')
        model_id = Model.objects.all().filter(brand_id=brand_id)
        cars = Car.objects.filter(model_id__in=model_id)
        # print(cars)

    # by transmission
    if request.GET.get('transmission'):
        transmission = request.GET.get('transmission')
        cars = Car.objects.filter(transmission__icontains=transmission)
        # print(cars)

    # by no of owner
    if request.GET.get('owner'):
        owner = request.GET.get('owner')
        cars = Car.objects.filter(no_of_owner=owner)

    # by price
    if request.GET.get('price'):
        price = request.GET.get('price')

        if price == '200000':
            cars = Car.objects.filter(price__lt=price)

        if price == '500000':
           cars = Car.objects.filter(price__gte='200000', price__lt=price)

        if price == '1000000':
            cars = Car.objects.filter(price__gte='500000', price__lt=price)


    paginator = Paginator(cars, 6)
    page_number = request.GET.get('page') 
    page_obj = paginator.get_page(page_number)
    totalpage = page_obj.paginator.num_pages
    

    context = { 'car': page_obj, 
                'lastpage': totalpage,
                'totalpagelist': [n+1 for n in range(totalpage)],
                # 'reviews': reviews,
                'brands': brands
            }

    # print(context)


    # Inquiry Form 
    if request.method == 'POST' and request.POST.get('inq_text', '') != '':
        if request.user.is_authenticated:
            inq = UserInquiry(request.POST) 
            if inq.is_valid():
                    instance = inq.save(commit=False)
                    instance.user_id = request.user
                    instance.save()
                    messages.success(request, 'We have got your query. will you connect soon!')
                    return redirect('home')
            else:
                messages.warning(request, 'plz, enter correct detials')
        else:
            return redirect('login')
            
        return redirect('home')


    # Post request for car search
    if request.method == 'POST' and request.POST.get('search', '') != '':
        print('post')
        search = request.POST['search']

        cars = Car.objects.filter(car_name__icontains=search, sold_out=0)

        paginator = Paginator(cars, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        totalpage = page_obj.paginator.num_pages

        context = { 'car': page_obj, 
                    'lastpage': totalpage,
                    'totalpagelist': [n+1 for n in range(totalpage)],
                    # 'reviews': reviews,
                    'brands': brands
                }
    
        # print(context)

    
    return render(request, 'home.html', context)



category = ''
start_date = ''
end_date = ''

# report generate
def generate_report(request):
    if request.user.is_superuser:     
        global category
        global start_date
        global end_date

        if request.method == 'POST':
            category = request.POST.get('category')
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            title = ''            
            
            if start_date > end_date:
                messages.warning(request, 'Start date should be less than end date !!')
                return redirect('generate-report')

            if category == 'user':
                users = User.objects.filter(date_joined__gte=start_date)
                user_phones = Profile.objects.filter(user__in=users.values('id'))
                title = 'User Report'
                context = { 'title': title, 'users': users, 'user_phones': user_phones}

            elif category == 'sell':
                title = 'Sells Report'
                # sells = CompanySell.objects.all()
                sells = Order.objects.filter(is_paid=True)
                cars = Car.objects.filter(car_id__in=sells.values('car_id'))
                context = {'title': title, 'sells': sells, 'cars': cars}

            elif category == 'purchase':
                title = 'Purchase Report'
                purchases = CompanyPurchase.objects.all()
                # purchases = Car.objects.all()
                cars = CarRequest.objects.filter(car_request_id__in=purchases.values('car_request_id')) 
                context = {'title': title, 'cars': cars, 'purchases': purchases}
            
            return render(request, 'pdf.html', context)
        else:
            return render(request, 'report.html')
    else:
        return render(request, '_404.html')


# download report 
def download_report(request):
    if request.user.is_superuser:          
        
        global category
        global start_date
        global end_date

        if category == 'user':
            users = User.objects.filter(date_joined__gte=start_date)
            user_phones = Profile.objects.filter(user__in=users.values('id'))
            title = 'User Report'
            context = { 'title': title, 'users': users, 'user_phones': user_phones}

        elif category == 'sell':
            title = 'Sells Report'
            # sells = CompanySell.objects.all()
            sells = Order.objects.filter(is_paid=True)
            cars = Car.objects.filter(car_id__in=sells.values('car_id'))
            context = {'title': title, 'sells': sells, 'cars': cars}

        elif category == 'purchase':
            title = 'Purchase Report'
            purchases = CompanyPurchase.objects.all()   
            cars = CarRequest.objects.filter(car_request_id__in=purchases.values('car_request_id'))
            context = {'title': title, 'cars': cars, 'purchases': purchases}

        template = get_template('pdf.html')
        html = template.render(context)
        result = BytesIO()

        pdf = pisa.pisaDocument(BytesIO(html.encode('ISO-8859-1')), result)

        if not pdf.err:
            return HttpResponse(result.getvalue(), content_type='application/pdf')
        else:
            return HttpResponse('Error')
    else:
        return render(request, 'report.html')


# 404 page
def error_404_view(request, exception):
    return render(request, '_404.html')
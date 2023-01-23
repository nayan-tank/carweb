from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.contrib import messages
from shop.models import *
from shop.forms import *
# from django.db.models import Q

# home 
def home(request):
    # get request for car
    cars = Car.objects.filter(sold_out=0)
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
        print(cars)

    # by transmission
    if request.GET.get('transmission'):
        transmission = request.GET.get('transmission')
        cars = Car.objects.filter(transmission__icontains=transmission)
        print(cars)

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
                'reviews': reviews,
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
                    'reviews': reviews,
                    'brands': brands
                }

        # print(context)
    
    return render(request, 'home.html', context)



# report generate
def generate_report(request):
    return HttpResponse("Report")

# 404 page
def error_404_view(request, exception):
    return render(request, '_404.html')
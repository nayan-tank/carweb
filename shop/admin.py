from django.contrib import admin
from .models import *
from datetime import datetime
from django.http import HttpResponse
# from django.contrib.auth.models import User

# Register your models here

# Company
@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    actions = ['custom_action']

    def custom_action(self, request, queryset):
        # do something with the selected queryset
        # for example you can update some fields, send an email etc
        queryset.update(name='Car Space')
    custom_action.short_description = "Update Name to Car Space"

    # list_display = [field.name for field in Company._meta.get_fields()]
    list_display = ['company_id', 'name', 'address', 'contact', 'email']
    search_fields = ('name',)


# # Area
# @admin.register(Area)
# class AreaAdmin(admin.ModelAdmin):
#     # list_display = [field.name for field in Area._meta.get_fields()]
#     list_display = ['area_pincode', 'area_name', 'city_id' ]
#     list_editable = ('area_name',)
#     search_fields = ('area_name',)
    

# # City
# @admin.register(City)
# class CityAdmin(admin.ModelAdmin):
#     # list_display = [field.name for field in City._meta.get_fields()]
#     list_display = ['city_id', 'city_name']
#     list_editable = ('city_name',)
#     search_fields = ('city_name',)


# UserProfile
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'otp', 'is_verified', 'show_profile']


# Order
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['amount', 'status', 'is_paid', 'user_id', 'car_id', 'datetime', 'instamojo_response']


# Brand
@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['brand_id', 'brand_name']
    search_fields = ('brand_name',)


# Model
@admin.register(Model)
class ModelAdmin(admin.ModelAdmin):
    list_display = ['model_id', 'model_name', 'year', 'engine', 'description', 'brand_id']
    search_fields = ('model_name',)
    list_per_page = 10
    list_filter = ('brand_id', )


# Car
@admin.register(Car)
class CarAdmin(admin.ModelAdmin):

    list_display = [ 'car_id', 'show_image', "sold_out",'car_name', 'price', 'color', 'reg_num', 'km_driven', 'seats', 'fuel_type', 'purc_date', 'no_of_owner', 'transmission', 'model_id', ]
    search_fields = ('car_name', 'color', 'price', 'fuel_type', 'transmission')
    list_per_page = 10
    list_filter = ('model_id',  'color', 'transmission',)

    # fields = ( 'show_image', )
    # readonly_fields = ('show_image',)
    
    # actions = ['generate_yearly_sales_report']

    # def generate_yearly_sales_report(self, request, queryset):
    #     # Generate the report using the queryset
    #     # For example, you can use pandas to generate a CSV file  
    #     data = queryset.filter(purc_date__year=datetime.now().year)
    #     df = pd.DataFrame.from_records(data.values())
    #     response = HttpResponse(df.to_csv(), content_type='text/html')
    #     response['Content-Disposition'] = 'attachment; filename="yearly_sales_report.csv"'
    #     return response
    # generate_yearly_sales_report.short_description = "Generate Yearly Sales Report"



# # Company sell
# @admin.register(CompanySell)
# class CompanySellAdmin(admin.ModelAdmin):
#     list_display = [ 'sell_id', 'sell_date', 'user_id', 'car_id' ]
#     search_fields = ('sell_date',)


# Company purchase
@admin.register(CompanyPurchase)
class CompanyPurchaseAdmin(admin.ModelAdmin):
    list_display = [ 'car_request_id', 'user_id', 'purc_date' ]
    search_fields = ('purc_date',)


# Image
@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['image_id', 'show_image', 'car_id', ]
    search_fields = ('car_id',)


# Request Car Image
@admin.register(RequestCarImage)
class RequestCarImageAdmin(admin.ModelAdmin):
    list_display = ['req_image_id', 'show_image', 'car_req_id', ]
    search_fields = ('car_req_id',)



# Car request
@admin.register(CarRequest)
class CarRequestAdmin(admin.ModelAdmin):
    list_display = [ 'car_request_id', 'car_name', 'car_price', 'fuel_type', 'status', 'color', 'km_driven', 'model_name', 'transmission', 'user_id' ]
    search_fields = ('car_name', 'color', 'car_price', 'fuel_type', 'model_name', 'transmission')
    list_per_page = 10
    list_filter = ('model_name', 'color', 'transmission', )


# # Car parts
# @admin.register(CarParts)
# class CarPartsAdmin(admin.ModelAdmin):
#     list_display = ['car_parts_id', 'part_name', 'price', 'car_request_id']
#     search_fields = ('part_name',)
#     list_filter = ('car_request_id', )


# Inquiry
@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = [ 'inquiry_id', 'email', 'inq_text', 'date_time', 'user_id' ]
    search_fields = ('email', 'inq_text')


# Complain
@admin.register(Complain)
class ComplainAdmin(admin.ModelAdmin):
    list_display = ['complain_id', 'subject', 'complain_text', 'date_time', 'user_id' ]
    search_fields = ('subject',)


# # Review
# @admin.register(Review)
# class ReviewAdmin(admin.ModelAdmin):
#     list_display = [ 'review_id', 'review_text', 'date_time', 'user_id' ]
#     search_fields = ('review_text', )
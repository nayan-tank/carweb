from django.core.exceptions import ValidationError
import re

from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa
from datetime import datetime
from django.conf import settings 

# clean city name
def clean_city_name(value):
    if not value.isalpha():
        raise ValidationError('city name must be string')


# clean area pincode
def clean_area_pincode(value):
    if not value.isnumeric():
        raise ValidationError('area pincode must be number')

# clean area name
def clean_area_name(value):
    if value.isnumeric():
        raise ValidationError('area name should not be number')


# clean brand name
def clean_brand_name(value):
    if value.isnumeric():
        raise ValidationError('brand name must be string')

# clean contact
def clean_contact(value):
    if not value.isnumeric():
        raise ValidationError('contact name must be number')

# clean color
def clean_color(value):
    if not value.isalpha():
        raise ValidationError('color name must be string')

# clean registration no
def clean_regno(value):
    if value.isnumeric() or value.isalpha():
        raise ValidationError('registration no must be alpha numeric')

# clean car name
def clean_car_name(value):
     if value.isnumeric():
        raise ValidationError('car name must be numeric')

# clean fuel type
def clean_fuel_type(value):
    if not value.isalpha():
        raise ValidationError('fuel type must be string')

# clean model name
def clean_model_name(value):
    if value.isnumeric():
        raise ValidationError('model name can not be numeric')

# clean transmission
def clean_transmission(value):
    if not value.isalpha():
        raise ValidationError('transmission name must be string')

# clean transmission
def clean_car_parts(value):
    if value.isnumeric():
        raise ValidationError('car parts can not be numeric')

# clean inquiry text
def clean_inq_text(value):
    if value.isnumeric():
        raise ValidationError('Enter a valid inquiry text !!')  

# clean complain subject
def clean_complain_sub(value):
    if value.isnumeric():
        raise ValidationError('Enter a valid subject text !!')

# clean complain text
def clean_complain_text(value):
    if value.isnumeric():
        raise ValidationError('Enter a valid complain text !!')

# clean feedback text
def clean_review_text(value):
    if value.isnumeric():
        raise ValidationError('Enter a valid review text !!')

# validate emoji
def validate_no_emoji(value):
        emoji_pattern = re.compile("["
            u"\U0001f600-\U0001f64f"  # emoticons
            u"\U0001f300-\U0001f5ff"  # symbols & pictographs
            u"\U0001f680-\U0001f6ff"  # transport & map symbols
            u"\U0001f1e0-\U0001f1ff"  # flags (iOS)
                               "]+", flags=re.UNICODE)
        if emoji_pattern.search(value) is not None:
            raise ValidationError("Emojis are not allowed in this field. Please insert text only.")

# validate phone no
def clean_phone(value):
    if not value.isnumeric:
        raise ValidationError('Length shoud be integer')


# generate PDF 
# def save_pdf(params: dict):
#     template = get_template('pdf.html')

#     html = template.render(params)
#     response = BytesIO()
#     pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8'), ), response)
#     pdf_name = str(datetime.now())

#     try:
#         with open(str(setting.BASE_DIR) + f'/media/pdf/{pdf_name}.pdf', 'wb+') as output:
#             pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8'), ), output)
    
#     except Exception as e:
#         print(e)

#     if pdf.err:
#         return '', False

#     return pdf_name, True







def clean_username(value):
        if ' ' in value:
            raise ValidationError("username can't contain space")

        return value


    # last name
def clean_first_name(value):
    
    if not value.isalpha():
        raise ValidationError('firstname can not contain number')

    return value

# first name
def clean_last_name(value):
    
    if not value.isalpha():
        raise ValidationError('lastname can not contain number')

    return value

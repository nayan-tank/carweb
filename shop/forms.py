from .models import *
from django import forms
from django.contrib.auth.models import User as AuthUser
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
import re

##########################  Admin Forms ##########################

# # Car 
# class CarForm(forms.ModelForm):
#     # images = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
#     class Meta:
#         model = Car
#         fields = '__all__'
#         widgets = {'image_url': forms.ClearableFileInput(attrs={'multiple': True})}



##########################  User Forms ##########################

# sing up 
class SignUpForm(UserCreationForm):
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput, required=True)
    phone_number = forms.CharField(max_length=10, required=True)
    avatar = forms.ImageField()

    class Meta:
        model = AuthUser
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_number', 'avatar']


    # username
    def clean_username(self):
        username = self.cleaned_data['username']
       
        if not username.isalpha():
            raise ValidationError('username can not contain number')
      
        if ' ' in username:
            raise ValidationError("username can't contain space")

        return username


    # last name
    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
       
        if not first_name.isalpha():
            raise ValidationError('firstname can not contain number')

        return first_name


    # first name
    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
       
        if not last_name.isalpha():
            raise ValidationError('lastname can not contain number')
    
        return last_name

  
    # email
    def clean_email(self):
        email = self.cleaned_data.get('email')

        try:
            match = AuthUser.objects.get(email=email)
        except User.DoesNotExist:
            return email

        raise forms.ValidationError('This email address is already in use.')

   
    # password
    def clean_password1(self):
        password1 = self.cleaned_data['password1']
       
        if ' ' in password1:
            raise ValidationError("password can't contain space")
    
        return password1

    # phone
    def clean_phone(self):
        phone = self.cleaned_data['phone']
       
        if not phone.isnumeric():
            raise ValidationError('phone no must be number')

        return phone

    


# update user profile
class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}),validators=[validate_no_emoji])
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}), validators=[validate_no_emoji])
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}), validators=[validate_no_emoji])
    # phone = forms.CharField(max_length=10, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}), validators=[validate_no_emoji])
    # avatar = forms.ImageField()

    class Meta:
        model = AuthUser
        fields = ['username', 'first_name', 'last_name', 'email',]    
    
    # username
    def clean_username(self):
        username = self.cleaned_data['username']
       
        if ' ' in username:
            raise ValidationError("username can't contain space")

        return username


    # last name
    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
       
        if not first_name.isalpha():
            raise ValidationError('firstname can not contain number')

        return first_name

    # first name
    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
       
        if not last_name.isalpha():
            raise ValidationError('lastname can not contain number')

        return last_name


# complain
class UserComplain(forms.ModelForm):
    class Meta:
        model = Complain
        fields = ['subject', 'complain_text']
        exclude = ['user_id']


# feedback
class UserFeedback(forms.ModelForm):
    class Meta:
        model = Review
        fields = '__all__'
        exclude = ['user_id']

    
# car request
class UserRequest(forms.ModelForm):
    images = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    class Meta:
        model = CarRequest
        fields = '__all__'
        exclude = ['status', 'user_id']

    def clean_car_name(self):
        data = self.cleaned_data['car_name']
        if re.search(r'[\U0001f600-\U0001f64f]', data):
            raise forms.ValidationError("Sorry, emojis are not allowed.")
        return data


# inquiry
class UserInquiry(forms.ModelForm):
    class Meta:
        model = Inquiry
        fields = '__all__'
        exclude = ['user_id']

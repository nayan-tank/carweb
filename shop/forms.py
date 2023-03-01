from .models import *
from django import forms
from django.contrib.auth.models import User as AuthUser
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
import re

##########################  Admin Forms ##########################


##########################  User Forms ##########################

# sing up 
class SignUpForm(UserCreationForm):
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput, required=True, validators=[validate_no_emoji])
    phone = forms.CharField(max_length=10 ,label='Phone', required=True, validators=[clean_phone])

    class Meta:
        model = AuthUser
        fields = ['username', 'first_name', 'last_name', 'email', 'phone']
    

    # username
    def clean_username(self):
        username = self.cleaned_data['username']

        emoji_pattern = re.compile("["
            u"\U0001f600-\U0001f64f"  # emoticons
            u"\U0001f300-\U0001f5ff"  # symbols & pictographs
            u"\U0001f680-\U0001f6ff"  # transport & map symbols
            u"\U0001f1e0-\U0001f1ff"  # flags (iOS)
                               "]+", flags=re.UNICODE)
        if emoji_pattern.search(username) is not None:
            raise ValidationError("Emojis are not allowed in this field. Please insert text only.")
       
        if not username.isalpha():
            raise ValidationError('username can not contain number')
      
        if ' ' in username:
            raise ValidationError("username can't contain space")

        return username


    # last name
    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
       
        emoji_pattern = re.compile("["
            u"\U0001f600-\U0001f64f"  # emoticons
            u"\U0001f300-\U0001f5ff"  # symbols & pictographs
            u"\U0001f680-\U0001f6ff"  # transport & map symbols
            u"\U0001f1e0-\U0001f1ff"  # flags (iOS)
                               "]+", flags=re.UNICODE)
        if emoji_pattern.search(first_name) is not None:
            raise ValidationError("Emojis are not allowed in this field. Please insert text only.")

        if first_name == '':
            raise ValidationError('This field is required !!')

        if not first_name.isalpha():
            raise ValidationError('firstname can not contain number')

        return first_name


    # first name
    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']

        emoji_pattern = re.compile("["
            u"\U0001f600-\U0001f64f"  # emoticons
            u"\U0001f300-\U0001f5ff"  # symbols & pictographs
            u"\U0001f680-\U0001f6ff"  # transport & map symbols
            u"\U0001f1e0-\U0001f1ff"  # flags (iOS)
                               "]+", flags=re.UNICODE)
        if emoji_pattern.search(last_name) is not None:
            raise ValidationError("Emojis are not allowed in this field. Please insert text only.")
       
        if last_name == '':
            raise ValidationError('This field is required !!')

        if not last_name.isalpha():
            raise ValidationError('lastname can not contain number')
    
        return last_name

  
    # email
    def clean_email(self):
        email = self.cleaned_data.get('email')

        emoji_pattern = re.compile("["
            u"\U0001f600-\U0001f64f"  # emoticons
            u"\U0001f300-\U0001f5ff"  # symbols & pictographs
            u"\U0001f680-\U0001f6ff"  # transport & map symbols
            u"\U0001f1e0-\U0001f1ff"  # flags (iOS)
                               "]+", flags=re.UNICODE)
        if emoji_pattern.search(email) is not None:
            raise ValidationError("Emojis are not allowed in this field. Please insert text only.")

        if email == '':
            raise ValidationError('This field is required !!')

        try:
            match = AuthUser.objects.get(email=email)
        except User.DoesNotExist:
            return email

        raise forms.ValidationError('This email address is already in use.')

   
    # password
    def clean_password1(self):
        password1 = self.cleaned_data['password1']

        emoji_pattern = re.compile("["
            u"\U0001f600-\U0001f64f"  # emoticons
            u"\U0001f300-\U0001f5ff"  # symbols & pictographs
            u"\U0001f680-\U0001f6ff"  # transport & map symbols
            u"\U0001f1e0-\U0001f1ff"  # flags (iOS)
                               "]+", flags=re.UNICODE)
        if emoji_pattern.search(password1) is not None:
            raise ValidationError("Emojis are not allowed in this field. Please insert text only.")
       
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
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'pattern': '[a-zA-z]{3,}$'}),)
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'pattern':'[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$'}), )
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'pattern': '[a-zA-z]{3,}$'}), validators=[validate_no_emoji])
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'pattern': '[a-zA-z]{3,}$'}), validators=[validate_no_emoji])

    class Meta:
        model = AuthUser
        fields = ['username', 'first_name', 'last_name', 'email', ]    
    
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
    km_driven = forms.IntegerField(widget=forms.NumberInput(attrs={'min': 1}))

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

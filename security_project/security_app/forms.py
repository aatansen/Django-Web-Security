from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django_recaptcha.fields import ReCaptchaField
from crispy_forms.helper import FormHelper
from django import forms

# Create user 
class Create_user_form(UserCreationForm):
    helper=FormHelper()
    class Meta:
        model=User
        fields=['username','email','password1','password2']
    captcha = ReCaptchaField()
    
    def __init__(self,*args,**kwargs):
        super(Create_user_form,self).__init__(*args,**kwargs)
        self.helper=FormHelper()
        
    def clean_email(self):
        email=self.cleaned_data.get('email')
        
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email already registered")
        
        if len(email)<=300:
            raise forms.ValidationError("This email is too long")
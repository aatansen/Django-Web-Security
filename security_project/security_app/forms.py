from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django_recaptcha.fields import ReCaptchaField

# Create user 
class Create_user_form(UserCreationForm):
    class Meta:
        model=User
        fields=['username','email','password1','password2']
    captcha = ReCaptchaField()
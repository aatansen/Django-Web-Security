from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Create user 
class Create_user_form(UserCreationForm):
    class Meta:
        model=User
        fields=['username','email','password1','password2']
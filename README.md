<div align="center">
<h1>Django Web Security</h1>
</div>

## Context
- [Preparation](#preparation)
- [Superuser](#superuser)
- [User registration](#user-registration)
- [reCAPTCHA v2](#recaptcha-v2)
    - [reCAPTCHA Installation](#recaptcha-installation)
- [Secure Environment Variable](#secure-environment-variable)
- [2FA in Django](#2fa-in-django)
    - [2FA Integration](#2fa-integration)
    - [User logout & login required decorator](#user-logout--login-required-decorator)

### Preparation
- Create project 
    - `django-admin startproject security_project`
- Create app
    - `py manage.py startapp security_app`
- Register app `security_app` in `INSTALLED_APPS`
- Templates, URL's and Views
    - Create `templates` folder in `security_app` directory
    - Create `urls.py` in `security_app` directory
        ```py
        from django.urls import path
        urlpatterns = [
            
        ]
        ```
    - Include `security_app` urls in project `urls.py`
        ```py
        from django.contrib import admin
        from django.urls import path,include
        urlpatterns = [
            path('admin/', admin.site.urls),
            path('',include('security_app.urls'))
        ]
        ```
    - Views file `views.py` already exists in `security_app` directory
    - Create `home`,`register`,`dashboard` page and render it
- Configure static files
    - Go to `settings.py` and add those
        ```py
        STATIC_URL = '/static/'
        STATICFILES_DIRS=[BASE_DIR / 'static']

        MEDIA_URL='/images/'
        MEDIA_ROOT=BASE_DIR / 'static/images'
        ```
    - In `urls.py` in project directory setup static
        ```py
        from django.contrib import admin
        from django.urls import path,include
        from django.conf import settings
        from django.conf.urls.static import static

        urlpatterns = [
            path('admin/', admin.site.urls),
            path('',include('security_app.urls'))
        ]
        urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
        ```
- Adding bootstrap
    - Get a bootstrap theme from [Bootswatch](https://bootswatch.com/)
    - Add `bootstrap.min.css` & link it in `base.html`
    - Add jquery bootstrap cdn script

[⬆️ Go to top](#context)

### Superuser
- Run `py manage.py makemigrations` & `py manage.py migrate`
- Create superuser `py manage.py createsuperuser`

[⬆️ Go to top](#context)

### User registration
- Create `forms.py` in app directory
    ```py
    from django.contrib.auth.forms import UserCreationForm
    from django.contrib.auth.models import User

    # Create user 
    class Create_user_form(UserCreationForm):
        class Meta:
            model:User
            fields=['username','email','password1','password2']
    ```
- Now in `views.py` handle the form request
    ```py
    def register(request):
        if request.method=='POST':
            form=Create_user_form(request.POST)
            if form.is_valid():
                form.save()
                return redirect('')
        else:
            form=Create_user_form()
        context={
            'form':form
        }
        return render(request,'register.html',context)
    ```
- In `register.html` simple form design
    ```jinja
        <div class="container bg-white shadow-md p-5 form-layout">
            <h3>Create an account</h3>
            <h5>Secure your account today!</h5>
            <form action="" method="POST" autocomplete="off">
                {% csrf_token %}
                {{form.username}}
                <br><br>
                {{form.email}}
                <br><br>
                {{form.password1}}
                <br><br>
                {{form.password2}}
                <br><br>
                <button type="submit" class="btn btn-info btn-log w-100 btn-block p3">Create your account</button>
            </form>
            <br><br>

            <div class="text-center">
                <p>Already have an account?</p> <a href="{% url 'home' %}">Login</a>
            </div>
        </div>
    ```
- Install [django-crispy-forms](https://pypi.org/project/django-crispy-forms/)
    - `pip install django-crispy-forms==1.14.0`
- Read the [django-crispy-forms-docs](https://django-crispy-forms.readthedocs.io/en/latest/install.html)
    - Add `crispy_forms` in `INSTALLED_APPS`
    - Add `CRISPY_TEMPLATE_PACK= 'bootstrap4'` in `settings.py`
- Update `register.html`
    ```jinja
    {% load crispy_forms_tags %}
    <div class="container bg-white shadow-md p-5 form-layout">
        <h3>Create an account</h3>
        <h5>Secure your account today!</h5>
        <form action="" method="POST" autocomplete="off">
            {% csrf_token %}
            {{form.username|as_crispy_field}}
            <br><br>
            {{form.email|as_crispy_field}}
            <br><br>
            {{form.password1|as_crispy_field}}
            <br><br>
            {{form.password2|as_crispy_field}}
            <br><br>
            <button type="submit" class="btn btn-info btn-log w-100 btn-block p3">Create your account</button>
        </form>
        <br><br>

        <div class="text-center">
            <p>Already have an account?</p> <a href="{% url 'home' %}">Login</a>
        </div>
    </div>
    ```

[⬆️ Go to top](#context)

### reCAPTCHA v2
- A reCAPTCHA is a free service provided by Google that is used to protect websites against spam and abuse
- This is typically used on registration / sign up forms
- A `CAPTCHA` is effectively a `Turing test` that is used to tell the difference between a robot/bot against a human
- There are multiple versions of reCAPTCHA available

#### reCAPTCHA Installation
- Install [django-recaptcha](https://pypi.org/project/django-recaptcha/)
    - `pip install django-recaptcha`
- Add `django_recaptcha` in `INSTALLED_APPS`
    ```py
    INSTALLED_APPS = [
        ...,
        'django_recaptcha',
        ...
    ]
    ```
- Add `reCAPTCHA` keys in `settings.py`
    ```py
    RECAPTCHA_PUBLIC_KEY = ''
    RECAPTCHA_PRIVATE_KEY = ''
    ```
- Go to [Google reCAPTCHA](https://www.google.com/recaptcha/about/)
- Navigate to [v3 Admin Console](https://www.google.com/recaptcha/admin/create) and get keys
    - Choose `Challenge (v2) - Verify requests with a challenge`
    - Select `"I'm not a robot" Checkbox - Validate requests with the "I'm not a robot" checkbox`
- Now add captcha in `forms.py`
    ```py
    ...
    from django_recaptcha.fields import ReCaptchaField

    # Create user 
    class Create_user_form(UserCreationForm):
        ...
        captcha = ReCaptchaField()
    ```
- Add `{{form.captcha}}` in `register.html` to see the reCAPTCHA

[⬆️ Go to top](#context)

### Secure Environment Variable
- Install [python-decouple](https://pypi.org/project/python-decouple/)
    - `pip install python-decouple`
- Create `.env` file in same directory of `settings.py` and copy the secure variable to `.env` file
- Now in `settings.py` import `config`
    ```py
    from decouple import config
    DEBUG= config('DEBUG',cast=bool)
    ALLOWED_HOSTS= ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=lambda v: [s.strip() for s in v.split(',')])
    RECAPTCHA_PUBLIC_KEY= config('RECAPTCHA_PUBLIC_KEY')
    RECAPTCHA_PRIVATE_KEY= config('RECAPTCHA_PRIVATE_KEY')
    ```
    > for more details and casting check [python-decouple-docs](https://github.com/HBNetwork/python-decouple)

[⬆️ Go to top](#context)

### 2FA in Django
- Two-Factor Authentication or `2FA` is an extra layer of security that is added in
conjunction with a username and password
- Usually, it is in the form of a physical or virtual device - (phone)
- Users can utilize 2FA with an authenticator app or by mobile SMS's
- Authenticator apps provide users with a random token every 30 seconds or so, which is used to login to their account
- 2FA Apps
    - [Google Authenticator](https://play.google.com/store/apps/details?id=com.google.android.apps.authenticator2)
    - [Authy App](https://play.google.com/store/apps/details?id=com.authy.authy) & [Authy website](https://authy.com/)
    - [Microsoft Authenticator](https://play.google.com/store/apps/details?id=com.azure.authenticator)

[⬆️ Go to top](#context)

#### 2FA Integration
- Install [django-two-factor-auth](https://pypi.org/project/django-two-factor-auth/)
    - `pip install django-two-factor-auth`
- Read [django-two-factor-auth-docs](https://django-two-factor-auth.readthedocs.io/en/stable/installation.html)
    - Install `pip install django-two-factor-auth[phonenumbers]`
    - Add apps in `INSTALLED_APPS`
        ```py
        INSTALLED_APPS = [
            ...
            'django_otp',
            'django_otp.plugins.otp_static',
            'django_otp.plugins.otp_totp',
            'two_factor',
        ]
        ```
        > Note: There are more apps mentioned in docs
    - Add middleware (add it after `AuthenticationMiddleware`)
        ```py
        ...
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django_otp.middleware.OTPMiddleware',
        ...
        ```
    - Add 2FA `LOGIN_URL` & `LOGIN_REDIRECT_URL` in `settings.py`
        ```py
        LOGIN_URL = 'two_factor:login'
        LOGIN_REDIRECT_URL = 'dashboard'
        ```
    - Add url in project `urls.py`
        ```py
        from two_factor.urls import urlpatterns as tf_urls
        urlpatterns = [
        ...
        path('', include(tf_urls)),
        ]
        ```
    - Now add name url which is `two_factor:login` to navigate to login page

[⬆️ Go to top](#context)

#### Configure timezone & 2FA Setup
- Go to django admin page there is `Add TOTP device` in `TOTP devices` section. Here 2FA devices will be listed
- Set timezone `TIME_ZONE = 'Asia/Dhaka'` in settings. More timezone available at [tz database timezone](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)

[⬆️ Go to top](#context)

#### User logout & login required decorator
- Login required decorator
    ```py
    from django.contrib.auth.decorators import login_required
    @login_required
    ...
    ```
- User Logout
    ```py
    from django.contrib.auth.models import auth
    def user_logout(request):
    auth.logout(request)
    return redirect('home')
    ```

[⬆️ Go to top](#context)
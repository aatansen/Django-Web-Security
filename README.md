<div align="center">
<h1>Django Web Security</h1>
</div>

## Context
- [Preparation](#preparation)
- [Superuser](#superuser)
- [User registration](#user-registration)
- [reCAPTCHA v2](#recaptcha-v2)
    - [reCAPTCHA Installation](#recaptcha-installation)
- [Secure Environment Variable I](#secure-environment-variable-i)
- [2FA in Django](#2fa-in-django)
    - [2FA Integration](#2fa-integration)
    - [User logout & login required decorator](#user-logout--login-required-decorator)
    - [Overriding the 2FA default templates](#overriding-the-2fa-default-templates)
    - [2FA Backup Tokens](#2fa-backup-tokens)
    - [2FA Disable](#2fa-disable)
- [Session timeout](#session-timeout)
    - [Introduction](#introduction)
    - [Adding a session timeout](#adding-a-session-timeout)
- [Secure Environment Variable II](#secure-environment-variable-ii)
    - [Introduction](#introduction-1)
    - [Creating environment variables](#creating-environment-variables)
- [Manage brute force attacks](#manage-brute-force-attacks)
    - [Introduction](#introduction-2)
    - [Create an account-locked template](#create-an-account-locked-template)

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

### Secure Environment Variable I
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

#### Overriding the 2FA default templates
- Download [django-two-factor-auth source code](https://github.com/jazzband/django-two-factor-auth) or just go to installed package directory and navigate to `two_factor`
- Copy the content of the `templates` and `templatetags` directory to our app directory
    - `security_project\security_app\`
- Modify `_base.html` to modify the login page
    - To modify field use `_wizard_forms.html`
    - To modify button use `_wizard_actions.html`
- Modify `templatetags` for custom classes tag
- After modification we can link `two_factor:setup` and `two_factor:profile` to redirect to that page accordingly
- Change tolerance to `90` in `forms.py` of `two_factor` package
    - `env\Lib\site-packages\two_factor\forms.py`

[⬆️ Go to top](#context)

#### 2FA Backup Tokens
- Enable 2FA by clicking enable button which is linked to `two_factor:setup` and scan with google authenticator
- To get backup token navigate to 2FA profile setting page `two_factor:profile` and generate backup tokens to use it when device can't be used

[⬆️ Go to top](#context)

#### 2FA Disable
- It can be found in `two_factor:profile` page 
- Click disable by tick on sure message

[⬆️ Go to top](#context)

### Session timeout
#### Introduction
- Users often forget to log out of their accounts, hence leaving their account idle for
several hours
- If they forget to logout in a public environment, anyone can simply use their computer and make devastating changes
- Therefore, users should be logged out automatically if they remain idle for too long

[⬆️ Go to top](#context)

#### Adding a session timeout
- Install [django-auto-logout](https://pypi.org/project/django-auto-logout/)
    - `pip install django-auto-logout`
- Install [pytz](https://pypi.org/project/pytz/)
    - `pip install pytz`
- Add middleware
    ```py
    MIDDLEWARE = [
        ...
        'django_auto_logout.middleware.auto_logout',
    ]
    ```
- Add `context_processors`
    ```py
    'context_processors': [
        ...
        'django_auto_logout.context_processors.auto_logout_client',
    ],
    ```
- Add `AUTO_LOGOUT` in `settings.py`
    ```py
    from datetime import timedelta
    # Auto logout
    AUTO_LOGOUT = {
        'IDLE_TIME': timedelta(seconds=30),
        # 'SESSION_TIME': timedelta(minutes=30),
        # 'MESSAGE': 'The session has expired. Please login again to continue.',
        'REDIRECT_TO_LOGIN_IMMEDIATELY': True,
    }
    ```
- And add this in template `dashboard.html`:
    ```jinja
    {{ redirect_to_login_immediately }}
    ```

[⬆️ Go to top](#context)

### Secure Environment Variable II
#### Introduction
- An environment variable is a variable whose value is set outside of a program
- It is important to utilize environment variables in order to keep our sensitive data
from our application code
- NEVER! Deploy your application without setting environment variables for your
sensitive data

[⬆️ Go to top](#context)

#### Creating environment variables
- Install [python-environ](https://pypi.org/project/python-environ/)
    - `pip install python-environ`
- Copy and save secure variable inside `.env` file 
- Now in `settings.py` add these
    ```py
    import environ
    env=environ.Env()
    environ.Env.read_env()
    SECRET_KEY = env('SECRET_KEY')
    ```

[⬆️ Go to top](#context)

### Manage brute force attacks
#### Introduction
- A 'brute-force' attack is when another user attempts to login to your account by trying out multiple username and password combinations in the hope of guessing correctly
- These attackers use a 'trial-and-error' method 

[⬆️ Go to top](#context)

#### Create an account-locked template
- Create `account-locked.html` page
    ```jinja
    {% extends 'base.html' %}
    {% load static %}

    {% block content %}
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
    <br><br>

    <div class="container bg-white shadow-md p-5 form-layout">

        <div class="text-center">
            <i class="fa fa-lock fa-4x text-dark" aria-hidden="true"></i>
            <h4 class="text-uppercase">Account locked</h4>
            <p>You have been locked out of your account due to multiple failed login attempts</p>
            <p>You may re-attempt to login to your account after the expiry period.</p>
            <a class="btn btn-info" type="button"  href="{% url 'home' %}"> Return to Homepage </a>
        </div>

    </div>
    {% endblock content %}
    ```
    > Here font-awesome version 4.7 is used for locked icon
- Render and create url route

[⬆️ Go to top](#context)
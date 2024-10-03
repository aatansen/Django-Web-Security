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
- [Session timeout - Auto Logout](#session-timeout---auto-logout)
    - [Introduction](#introduction)
    - [Adding a session timeout](#adding-a-session-timeout)
    - [Session Timeout - Auto Logout Message](#session-timeout---auto-logout-message)
- [Secure Environment Variable II](#secure-environment-variable-ii)
    - [Introduction](#introduction-1)
    - [Creating environment variables](#creating-environment-variables)
- [Manage brute force attacks](#manage-brute-force-attacks)
    - [Introduction](#introduction-2)
    - [Create an account-locked template](#create-an-account-locked-template)
    - [Brute force prevent integration](#brute-force-prevent-integration)
    - [Brute force prevention - Custom functionality](#brute-force-prevention---custom-functionality)
- [Password Management](#password-management)
    - [Password Reset](#password-reset)
- [Django Messages](#django-messages)
    - [Session Timeout - Auto Logout Message](#session-timeout---auto-logout-message)
- [Custom Email Validations](#custom-email-validations)
    - [Adding favicon](#adding-a-favicon)
    - [User Email Validation](#user-email-validation)
- [Pre-Deployment Security](#pre-deployment-security)
- [File Handling](#file-handling)

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

### Session timeout - Auto Logout
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

#### Brute force prevent integration
- Install [django-axes](https://pypi.org/project/django-axes/)
    - `pip install django-axes`
- Go to [django-axes-docs](https://django-axes.readthedocs.io/en/latest/2_installation.html)
    - Add `'axes',` in `INSTALLED_APPS`
        ```py
        INSTALLED_APPS = [
            ...
            'axes',
        ]
        ```
    - Add `AUTHENTICATION_BACKENDS` in `settings.py`
        ```py
        AUTHENTICATION_BACKENDS = [
            # AxesStandaloneBackend should be the first backend in the AUTHENTICATION_BACKENDS list.
            'axes.backends.AxesStandaloneBackend',

            # Django ModelBackend is the default authentication backend.
            'django.contrib.auth.backends.ModelBackend',
        ]
        ```
    - Add `MIDDLEWARE`
        ```py
        MIDDLEWARE = [
            ...
            'axes.middleware.AxesMiddleware',
        ]
        ```
    - Add axes configuration settings
        ```py
        # Axes configuration settings
        AXES_FAILURE_LIMIT: 3 # How many times a user can fail a login
        AXES_COOLOFF_TIME: 2 # Wait 2 hours before attempting to login again 
        AXES_RESET_ON_SUCCESS = True # Reset failed login attempts 
        AXES_LOCKOUT_TEMPLATE = 'account-locked.html' # Add a custom template on failure 
        ```
    - Now `py manage.py check` to see any error
    - Finally `py manage.py migrate` and run the server
- To reset restriction
    - `py manage.py axes_reset`

[⬆️ Go to top](#context)

#### Brute force prevention - Custom functionality
- Read the [customizing axes docs](https://django-axes.readthedocs.io/en/latest/5_customization.html#customizing-lockout-parameters)
    - Using `username` to identify the user for lockout purposes
        ```py
        # Axes additional configurations
        AXES_LOCKOUT_PARAMETERS = ["username"]
        ```

[⬆️ Go to top](#context)

### Password Management
#### Password Reset
- Setup url/views in `urls.py`
    ```py
    # password reset 
    from django.contrib.auth import views as auth_views

    urlpatterns = [
        ...
        # password reset 
        # email submit form
        path('reset_password/',auth_views.PasswordResetView.as_view(),name='reset_password'),
        # Reset message
        path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
        # Link for password reset
        path('reset/<uidb64>/<token>',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
        # Password changed success message
        path('password_reset_complete/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
        
    ]
    ```
- Add configuration in `settings.py`
    ```py
    # Password reset
    EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST='smtp.gmail.com'
    EMAIL_PORT='587'
    EMAIL_USE_TLS='True'

    EMAIL_HOST_USER=''
    EMAIL_HOST_PASSWORD=''
    DEFAULT_FROM_EMAIL=''
    ```
- For gmail configuration backend we need app password
    - Go to [Google my account apppasswords](https://myaccount.google.com/apppasswords)
    - Create a new app and get the password and fill-up below config
        ```py
        EMAIL_HOST_USER=''
        EMAIL_HOST_PASSWORD=''
        DEFAULT_FROM_EMAIL=''
        ```
- Now to modify default view template of reset password page
    - Create a directory in templates `password_reset`
    - Create `password-reset.html`, `password-reset-sent.html`, `password-reset-form.html`, `password-reset-complete.html`
    - Now in `urls.py` set `template_name` argument in `as_view` for each created password pages
        - `as_view(template_name='password_reset/password-reset.html')`
        - ...
- Now we will be able to reset password

[⬆️ Go to top](#context)

### Django Messages
- Import django message
    - `from django.contrib import messages`
- Add messages where required `messages.success(request,"Logout success!")`
- More tag can be found in [django-message-tags](https://docs.djangoproject.com/en/5.1/ref/contrib/messages/#message-tags)
- Create a html file in templates directory `messages.html`
    ```jinja
    {% if messages %}
    {% for message in messages %}
        {% if message.tags == 'success' %}
        <p>{{ message }}</p>
        {% endif %}
    {% endfor %}
    {% endif %}
    ```
    - We can also use `{% if message.level == DEFAULT_MESSAGE_LEVELS.SUCCESS %}`
- To style the message
    - `<p id="message-timer" class="alert alert-success float-center text-center"> <i class="fa fa-check" aria-hidden="true"></i> &nbsp; {{message}} </p>`
    - Here `message-timer` id will be used in `scripts.js` to make the message disappear in 2 seconds
        ```js
        var message_timeout = document.getElementById("message-timer");

        setTimeout(function () {
        message_timeout.style.display = "none";
        }, 5000);
        ```
    - Make sure to add the `scripts.js` in `base.html`
        - `<script src="{% static 'js/scripts.js' %}"> </script>`

[⬆️ Go to top](#context)

#### Session Timeout - Auto Logout Message
- Update `settings.py` and add `MESSAGE` in `AUTO_LOGOUT`
    ```py
    # Auto logout
    AUTO_LOGOUT = {
        'IDLE_TIME': timedelta(seconds=5),
        # 'SESSION_TIME': timedelta(minutes=30),
        'MESSAGE': 'The session has expired. Please login again to continue.',
        'REDIRECT_TO_LOGIN_IMMEDIATELY': True,
    }
    ```
- Add message `info` tag in `messages.html`
    ```jinja
    ...
    {% elif message.tags == 'info' %}
        <div class="message alert alert-info float-center text-center {{ message.tags }}">
      <i class="fa fa-clock-o" aria-hidden="true"></i> &nbsp; {{ message }}
    </div>
    ...
    ```
- Include `messages.html` in `two_factor` login page `_base.html`
    ```jinja
    ...
    {% include 'messages.html' %}
    ...
    ```
- Now the message will be shown when auto logout

[⬆️ Go to top](#context)

### Custom Email Validations
#### Adding a favicon
- Go to [favicon](https://favicon.io/)
- Generate Text to favicon
- Add favicon files in static `images` directory
- Add those in `base.html`
    ```html
    <!-- Favicon -->
    <link rel="icon" type="image/png" sizes="32x32" href="{% static 'images/small-favicon.png' %}">
    <link rel="icon" type="image/png" sizes="16x16" href="{% static 'images/large-favicon.png' %}">
    ```

[⬆️ Go to top](#context)

#### User Email Validation
- Using Crispy form FormHelper
    ```py
    ...
    from crispy_forms.helper import FormHelper
    from django import forms

    # Create user 
    class Create_user_form(UserCreationForm):
        helper=FormHelper()
        ...
        
        def __init__(self,*args,**kwargs):
            super(Create_user_form,self).__init__(*args,**kwargs)
            self.helper=FormHelper()
            
        def clean_email(self):
            email=self.cleaned_data.get('email')
            
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError("This email already registered")
            
            if len(email)<=300:
                raise forms.ValidationError("This email is too long")
    ```

[⬆️ Go to top](#context)

### Pre-Deployment Security
- Make sure `DEBUG=False`
- Add `ALLOWED_HOSTS`
- Check any issue before deploy `py manage.py check --deploy`
    ```text
    WARNINGS:
    ?: (security.W004) You have not set a value for the SECURE_HSTS_SECONDS setting. If your entire site is served only over SSL, you may want to consider setting a value and enabling HTTP Strict Transport Security. Be sure to read the documentation first; enabling HSTS carelessly can cause serious, irreversible problems.
    ?: (security.W008) Your SECURE_SSL_REDIRECT setting is not set to True. Unless your site should be available over both SSL and non-SSL connections, you may want to either set this setting True or configure a load balancer or reverse-proxy server to redirect all connections to HTTPS.
    ?: (security.W012) SESSION_COOKIE_SECURE is not set to True. Using a secure-only session cookie makes it more difficult for network traffic sniffers to hijack user sessions.
    ?: (security.W016) You have 'django.middleware.csrf.CsrfViewMiddleware' in your MIDDLEWARE, but you have not set CSRF_COOKIE_SECURE to True. Using a secure-only CSRF cookie makes it more difficult for network traffic sniffers to steal the CSRF token.
    ?: (security.W018) You should not have DEBUG set to True in deployment.
    ```
- This will only work in deployment server
    ```py
    # Deployment settings 
    # Protection against XSS attacks
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True

    # CSRF Protection
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIES_SECURE = True

    # SSL redirect
    SECURE_SSL_REDIRECT = True

    # Enable HSTS
    SECURE_HSTS_SECONDS = 86400
    SECURE_HSTS_PRELOAD = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    ```
- Change admin site url route
- Check website using [Mozilla Observatory](https://observatory.mozilla.org/), [DJ Checkup](https://djcheckup.com/)
- Also check [CSP](https://pypi.org/project/django-csp/) (Content Security policy)

[⬆️ Go to top](#context)

### File Handling
- Good file management principles to research and to integrate in Django web application would include to:
    - Only allow registered users to upload files
    - Limit the number of characters in an uploaded file's name
    - Limit the size of an uploaded file
    - Rename a user's file name upon upload
    - Validate the file's extension (.pdf) to ensure it isn't a type of malware


[⬆️ Go to top](#context)

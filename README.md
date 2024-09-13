<div align="center">
<h1>Django Web Security</h1>
</div>

## Context
- [Preparation](#preparation)
- [Superuser](#superuser)
- [User registration](#user-registration)

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
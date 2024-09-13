<div align="center">
<h1>Django Web Security</h1>
</div>

## Context
- [Preparation](#preparation)

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
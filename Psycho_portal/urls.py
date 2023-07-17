"""
URL configuration for Psycho_portal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from users import views as users_view
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('api/', include('api.urls')),
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path('fear_tracker/', include('fear_tracker.urls')),
    path('psycho_tests/', include('psycho_tests.urls')),
    path('profile/', users_view.profile, name='profile'),
    path('register/', users_view.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# TODO: (DONE) modify template folders
# TODO: (DONE) center pagination
# TODO: (DONE) after viewing post add button to get back to all posts
# TODO: (DONE) change plots for plotly (dynamically created)
# TODO: (DONE) add photo for users
# TODO: (DONE) center profile picture and delete in post details click on author
# TODO: (DONE) modify models for tests/questions
# TODO: (DONE) add possibility for user to create own test
# TODO: (DANE) all tests visible at one endpoint
# TODO: (DONE) user is able to complete any test
# -------------------------------------

# TODO: (DONE) Modify creating tests, user should be able to set custom answers
# TODO: (DONE) add possibility to see results from all tests (report)
# TODO: (DONE) user is able to delete records from db for plot
# TODO: (DONE) add possibility to delete tests created by user
# TODO: (DONE) Mypy + django-stubs
# TODO: (DONE) REST API for creating tests
# -------------------------------------

# TODO: () modify answer model to have one row for all answers
# TODO: () modify rest api into 3 endpoints


# array field dla answer , jeden row dla wszystkich odpowiedzi stworzonych
# klucz do odpowiedz dac do psychotestu
# 3 endpointy dla api create


# TODO: Unit tests: blog(DONE), fear_tracker(views-missing), users(models missing), psycho_tests(), api()

# TODO: created psycho test should be accepted by admin, hierarchy of users and authorization
# TODO: add postgres db
# TODO: README
# TODO: Docker
# TODO: Pre-commit




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
                  path('admin/', admin.site.urls),
                  path('', include('blog.urls')),
                  path('fear_tracker/', include('fear_tracker.urls')),
                  path('personality_test/', include('personality_test.urls')),
                  path('profile/', users_view.profile, name='profile'),
                  path('register/', users_view.register, name='register'),
                  path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
                  path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# TODO: (DONE) modify templates folder
# TODO: (DONE) center pagination
# TODO: (DONE) after viewing post add button to get back to all posts
# TODO: (DONE) change plots for plotly (dynamically created)
# TODO: add photo for users
# TODO: add hierarchy of users and authentication
# TODO: modify models for tests/questions
# TODO: add possibility for user to create own test, accepted by admin
# TODO: all tests visible on one endpoint
# TODO: on profile endpoint add availability to see users test and able to update?
# TODO: REST API for creating tests
# TODO: Unit tests: blog(DONE), fear_tracker(), personality_test(), users()

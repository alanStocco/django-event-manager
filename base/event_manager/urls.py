"""
URL configuration for event_manager project.

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
from django.urls import path, include
from rest_framework import routers
from .views import *
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_simplejwt import views as jwt_views


urlpatterns = [
    # User registration
    path('register/', register_user, name='user-register'),

    # # User login
    path('login/', login_user, name='user-login'),

    # override sjwt stock token
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),

    # # User logout
    path('logout/', logout_user, name='user-logout'),

    # # Event creation
    path('events/create/', create_event, name='event-create'),

    # # User events
    path('events/user/', fetch_user_events, name='user-events'),

    # # All events
    path('events/', list_events, name='all-events'),

    # # Event editing
    path('events/<int:event_id>/edit/', edit_event, name='event-edit'),

    # # Event registration
    path('events/<int:event_id>/register/', register_event, name='event-register'),

    # # Event unregistration
    path('events/<int:event_id>/unregister/', unregister_event, name='event-unregister'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
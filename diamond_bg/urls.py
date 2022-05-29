"""diamond_bg URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.template.defaulttags import url
from django.urls import path, include

# from file.views import generate_qrcode

urlpatterns = [
    path('api/user/', include(('user.urls', 'user'))),
    path('api/file/', include(('file.urls', 'file'))),
    path('api/team/', include(('team.urls', 'team'))),
    path('api/message/', include(('message.urls', 'message'))),
    path('api/favourite/', include(('favourite.urls', 'favourite'))),

]

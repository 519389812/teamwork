"""teamwork URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, re_path
import announcement.views as announcement_view
from django.views.static import serve
from teamwork import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', announcement_view.login, name='login'),
    re_path('^announcement/(\d+)$', announcement_view.make_announcement),
    re_path('^readconfirm/(\d+)/(.*)$', announcement_view.read_confirm, name='read_confirm'),
    re_path('^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path('^showupload/(\d+)/(.*)$', announcement_view.show_upload, name='show_upload'),
    re_path('^feedbackconfirm/(\d+)$', announcement_view.feedback_confirm, name='feedback_confirm'),
]

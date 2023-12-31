"""wb_scripts URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from blog import api
from wb_scripts.settings import base

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls', namespace='blog')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('api-bot/get-category/', api.GetCategory.as_view()),
    path('api-bot/get-category-posts/', api.GetPostList.as_view()),
    path('api-bot/get-post-scripts/', api.GetScriptList.as_view()),
    path('api-bot/get-script/', api.GetScript.as_view()),
    path('api-bot/register-user/', api.RegisterUser.as_view()),
    path('api-bot/reset-password/', api.ResetPassword.as_view()),
]
urlpatterns += static(base.STATIC_URL, document_root=base.STATIC_ROOT)
urlpatterns += static(base.MEDIA_URL, document_root=base.MEDIA_ROOT)

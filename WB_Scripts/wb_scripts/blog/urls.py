from django.urls import path
from django.contrib.auth import views as views_auth
from . import views
from .forms import UserLoginForm

app_name = 'blog'
urlpatterns = [
    # post views
    path("", views.index, name="index"),
    path('category/<int:id_>-<str:slug>/', views.category_page, name='category_page'),
    path('post/<int:id_>-<str:slug>/', views.post_detail, name='post_detail'),
    path('news/', views.news_list_page, name='news_list_page'),
    path('news/<int:id_>-<str:slug>/', views.news_detail, name='news_detail'),
    path('search/', views.search, name='search'),
    path('login/', views_auth.LoginView.as_view(authentication_form=UserLoginForm), name='login'),
]

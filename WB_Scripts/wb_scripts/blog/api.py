from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework.views import APIView

from blog.models import Category, Post, ScriptsForPosts, ExtendedUser
from blog.serializers import CategorySerializer, PostSerializer, ScriptSerializer


class GetCategory(APIView):
    @staticmethod
    def get(request):
        category_parent = request.GET.get('parent')
        if category_parent == '0':
            category = Category.cat_man.get_queryset()
        else:
            category = Category.cat_man.get_queryset(category_parent)
        serialized_category = CategorySerializer(category, many=True)
        return Response(serialized_category.data)


class GetPostList(APIView):
    @staticmethod
    def get(request):
        category_posts = request.GET.get('category_posts')
        post_list = Post.post_man.get_sub_category_posts(category_posts)
        serialized_posts = PostSerializer(post_list, many=True)
        return Response(serialized_posts.data)


class GetScriptList(APIView):
    @staticmethod
    def get(request):
        post_id = request.GET.get('post_id')
        scripts_list = ScriptsForPosts.scr_man.get_related_scripts(post_id)
        serialized_scripts = ScriptSerializer(scripts_list, many=True)
        return Response(serialized_scripts.data)


class GetScript(APIView):
    @staticmethod
    def get(request):
        script_id = request.GET.get('script_id')
        script = ScriptsForPosts.scr_man.get_script(script_id)
        serialized_script = ScriptSerializer(script, many=True)
        return Response(serialized_script.data)


class RegisterUser(APIView):
    @staticmethod
    def post(request):
        username = request.data['username']
        telegram_id = request.data['telegram_id']
        password = BaseUserManager().make_random_password()
        safe_password = make_password(password)
        user_obj = User(
            username=username,
            password=safe_password)
        user_obj.save()
        user = ExtendedUser.objects.create(user_id=user_obj.pk, telegram_id=telegram_id)
        return Response({"username": username,
                         "password": password})

    @staticmethod
    def get(request):
        telegram_id = request.GET.get('telegram_id')
        try:
            user = ExtendedUser.objects.get(telegram_id=telegram_id)
            return Response(status=200)
        except ObjectDoesNotExist:
            return Response(status=404)


class ResetPassword(APIView):
    @staticmethod
    def get(request):
        telegram_id = request.GET.get('telegram_id')
        user: ExtendedUser = ExtendedUser.objects.get(telegram_id=telegram_id)
        password = BaseUserManager().make_random_password()
        a = User.set_password(user.user, password)
        User.save(user.user)
        return Response(data={"username": user.user.username,
                              "password": password})

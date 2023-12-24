from rest_framework.serializers import ModelSerializer

from blog.models import Category, Post, ScriptsForPosts


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'parent']


class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'category', 'description']


class ScriptSerializer(ModelSerializer):
    class Meta:
        model = ScriptsForPosts
        fields = ['id', 'title', 'script', 'operation', 'type', 'post']

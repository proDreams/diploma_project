from django.contrib import admin

from .models import Post, Category, News, NewsForPosts, ScriptsForPosts, Feedback, ExtendedUser


class NewsForPostsInline(admin.StackedInline):
    model = NewsForPosts


class ScriptsInline(admin.StackedInline):
    model = ScriptsForPosts
    exclude = ("author",)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'category', 'publish', 'updated', 'status', 'view_count']
    list_filter = ['status', 'publish', 'author']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']
    exclude = ("author", 'view_count', 'publish')
    inlines = [NewsForPostsInline, ScriptsInline, ]

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        obj.save()


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'parent']
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title']


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    inlines = [NewsForPostsInline, ]
    list_display = ['title', 'slug', 'author', 'updated', 'view_count']
    prepopulated_fields = {'slug': ('title',)}
    exclude = ("author", 'view_count')

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        obj.save()


@admin.register(NewsForPosts)
class NewsForPostsAdmin(admin.ModelAdmin):
    list_display = ['news', 'post']


@admin.register(ScriptsForPosts)
class ScriptsForPostsAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'post', 'type']
    exclude = ["author"]

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        obj.save()


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['author', 'body']

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        obj.save()

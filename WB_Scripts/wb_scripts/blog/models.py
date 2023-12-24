from ckeditor_uploader.fields import RichTextUploadingField
from django.db.models import (Model,
                              Manager,
                              TextChoices,
                              CharField,
                              SlugField,
                              ForeignKey,
                              TextField,
                              DateTimeField,
                              Index,
                              CASCADE,
                              PROTECT,
                              IntegerField,
                              OneToOneField)
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User


class PostManager(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED).order_by('-updated')[:4]

    def get_most_visited(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED).order_by('-view_count')[:5]

    def get_sub_category_posts(self, category_id):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED,
                                             category=category_id).order_by('-publish')

    def get_post(self, post_id):
        return super().get_queryset().filter(id=post_id)


def create_recently_viewed_record(user_id, post_id):
    record = RecentlyPosts.rec_man.filter(user=user_id, post=post_id).order_by('-date_visit')
    if record:
        RecentlyPosts.rec_man.filter(id=record[0].id).update(date_visit=timezone.now())
    else:
        RecentlyPosts.rec_man.create(user_id=user_id, post_id=post_id, date_visit=timezone.now())


def increase_post_view_count(request: int):
    record = Post.objects.filter(id=request)
    record.update(view_count=record[0].view_count + 1)


def increase_news_view_count(request: int):
    record = News.news_man.filter(id=request)
    record.update(view_count=record[0].view_count + 1)


class RecentManager(Manager):
    def get_recently_posts(self, request):
        return super().filter(user=request).order_by('-date_visit')[:5]


class NewsManager(Manager):
    pass


class ScriptsManager(Manager):
    def get_related_scripts(self, request):
        return super().get_queryset().filter(post_id=request)

    def get_script(self, request):
        return super().get_queryset().filter(id=request)


class NewsForPostsManager(Manager):
    def get_related_posts(self, request):
        return super().get_queryset().filter(news_id=request)

    def get_related_news(self, request):
        return super().get_queryset().filter(post_id=request)

    def check_exists(self, post_id, news_id):
        return super().get_queryset().filter(post_id=post_id, news_id=news_id)


class CategoryManager(Manager):
    def get_queryset(self, parent=None):
        return super().get_queryset().filter(parent=parent)


class Category(Model):
    title = CharField(max_length=250,
                      verbose_name="Заголовок")
    slug = SlugField(max_length=250)
    parent = ForeignKey('self', on_delete=PROTECT, null=True, blank=True, related_name='children',
                        db_index=True, verbose_name='Родительская категория')

    objects = Manager()
    cat_man = CategoryManager()

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def get_absolute_url(self):
        return reverse('blog:category_page', args=[int(self.id), str(self.slug)])

    def __str__(self):
        return self.title


class Post(Model):
    class Status(TextChoices):
        DRAFT = 'ЧЕ', 'Черновик'
        PUBLISHED = 'ОП', 'Опубликовано'

    class ModelType:
        model_type = 'post'

    title = CharField(max_length=250,
                      verbose_name="Заголовок")
    slug = SlugField(max_length=250)
    author = ForeignKey(User,
                        on_delete=CASCADE,
                        related_name='blog_posts',
                        verbose_name="Автор")
    category = ForeignKey(Category,
                          on_delete=CASCADE,
                          default=1,
                          verbose_name="Категория")
    description = TextField(max_length=300)
    publish = DateTimeField(default=timezone.now,
                            verbose_name="Опубликовано")
    updated = DateTimeField(auto_now=True,
                            verbose_name="Обновлено")
    status = CharField(max_length=2,
                       choices=Status.choices,
                       default=Status.DRAFT,
                       verbose_name="Статус")
    view_count = IntegerField(default=1,
                              verbose_name="Количество просмотров")

    objects = Manager()
    post_man = PostManager()

    class Meta:
        ordering = ['-publish']
        indexes = [
            Index(fields=['-publish']),
        ]
        verbose_name = 'Материал'
        verbose_name_plural = 'Материалы'

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.id, self.slug])

    def __str__(self):
        return self.title


class RecentlyPosts(Model):
    user = ForeignKey(User,
                      on_delete=CASCADE,
                      default=1,
                      verbose_name="Пользователь")
    post = ForeignKey(Post,
                      on_delete=CASCADE,
                      default=1,
                      verbose_name="Материал")
    date_visit = DateTimeField(auto_now=True,
                               verbose_name="Дата просмотра")

    rec_man = RecentManager()


class News(Model):
    class ModelType:
        model_type = 'news'

    title = CharField(max_length=250,
                      verbose_name="Название новости")
    slug = SlugField(max_length=250)
    author = ForeignKey(User,
                        on_delete=CASCADE,
                        verbose_name="Автор новости")
    body = RichTextUploadingField(verbose_name="Содержание новости")
    publish = DateTimeField(default=timezone.now,
                            verbose_name="Опубликовано")
    updated = DateTimeField(auto_now=True,
                            verbose_name="Обновлено")
    view_count = IntegerField(default=1,
                              verbose_name="Количество просмотров")

    news_man = NewsManager()

    class Meta:
        ordering = ['-updated']
        indexes = [
            Index(fields=['-updated']),
        ]
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

    def get_absolute_url(self):
        return reverse('blog:news_detail', args=[self.id, self.slug])

    def __str__(self):
        return self.title


class NewsForPosts(Model):
    news = ForeignKey(News,
                      on_delete=CASCADE,
                      null=True,
                      verbose_name="Новость")
    post = ForeignKey(Post,
                      on_delete=CASCADE,
                      null=True,
                      verbose_name="Материал")

    nfp_man = NewsForPostsManager()

    class Meta:
        verbose_name = 'Связь новости и материала'
        verbose_name_plural = 'Связь новости и материала'


class ScriptsForPosts(Model):
    class Type(TextChoices):
        SCRIPT = 'SC', 'Скрипт'
        SUPERVISOR = 'SV', 'Супервайзер'
        PROBLEM = 'PR', 'Проблема'

    class ModelType:
        model_type = 'script'

    title = CharField(max_length=250,
                      verbose_name="Заголовок")
    author = ForeignKey(User,
                        on_delete=CASCADE,
                        verbose_name="Автор")
    script = TextField(verbose_name="Скрипт")
    operation = CharField(max_length=250, default='Нет информации',
                          verbose_name="Операция")
    post = ForeignKey(Post,
                      on_delete=CASCADE,
                      verbose_name="Материал")
    type = CharField(max_length=2,
                     choices=Type.choices,
                     default=Type.SCRIPT,
                     verbose_name="Тип скрипта")

    scr_man = ScriptsManager()

    class Meta:
        verbose_name = 'Скрипт и регистрация обращений'
        verbose_name_plural = 'Скрипты и регистрации обращений'


class Feedback(Model):
    author = ForeignKey(User,
                        on_delete=CASCADE,
                        verbose_name="Автор")
    body = TextField(verbose_name="Отзыв")

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class ExtendedUser(Model):
    user = OneToOneField(User, on_delete=CASCADE)
    color_scheme = CharField(max_length=100, default='dark')
    telegram_id = CharField(max_length=100, default=0)

    objects = Manager()

from django.contrib.auth.forms import UsernameField, AuthenticationForm
from django.forms import ModelForm, Textarea, Select, TextInput, PasswordInput, CharField, DateTimeInput

from blog.models import News, NewsForPosts, ScriptsForPosts, Feedback


class NewsForm(ModelForm):
    class Meta:
        model = News
        fields = ('title', 'body', 'publish')

        widgets = {
            'title': Textarea(attrs={'class': 'form-control', 'cols': 20, 'rows': 1}),
            'body': Textarea(attrs={'class': 'form-control', 'cols': 20, 'rows': 25}),
            'publish': DateTimeInput(attrs={'class': 'form-control', "type": "date"})
        }

    def __init__(self, *args, **kwargs):
        self._user = kwargs.pop('user')
        super(NewsForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        inst = super(NewsForm, self).save(commit=False)
        inst.author = self._user
        if commit:
            inst.save()
            self.save_m2m()
        return inst


class NewsForPostsForm(ModelForm):
    class Meta:
        model = NewsForPosts
        fields = ('post',)

        widgets = {
            'news': Select(attrs={'class': 'form-select', 'cols': 20, 'rows': 1}),
            'post': Select(attrs={'class': 'form-select', 'cols': 20, 'rows': 1}),
        }

    def __init__(self, *args, **kwargs):
        self.news = kwargs.pop('news_id')
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        inst = super(NewsForPostsForm, self).save(commit=False)
        inst.news_id = self.news
        if commit:
            inst.save()
            self.save_m2m()
        return inst


class PostsForNewsForm(ModelForm):
    class Meta:
        model = NewsForPosts
        fields = ('news',)

        widgets = {
            'news': Select(attrs={'class': 'form-select', 'cols': 20, 'rows': 1}),
            'post': Select(attrs={'class': 'form-select', 'cols': 20, 'rows': 1}),
        }

    def __init__(self, *args, **kwargs):
        self.post = kwargs.pop('post_id')
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        inst = super(PostsForNewsForm, self).save(commit=False)
        inst.post_id = self.post
        if commit:
            inst.save()
            self.save_m2m()
        return inst


class ScriptsForm(ModelForm):
    class Meta:
        model = ScriptsForPosts
        fields = ('title', 'script', 'operation', 'type')

        widgets = {
            'title': Textarea(attrs={'class': 'form-control', 'cols': 20, 'rows': 1}),
            'script': Textarea(attrs={'class': 'form-control', 'cols': 20, 'rows': 3}),
            'operation': Textarea(attrs={'class': 'form-control', 'cols': 20, 'rows': 2}),
            'post': Select(attrs={'class': 'form-select', 'cols': 20, 'rows': 1}),
            'type': Select(attrs={'class': 'form-select', 'cols': 20, 'rows': 1}),
        }

    def __init__(self, *args, **kwargs):
        self._user = kwargs.pop('user')
        self.post = kwargs.pop('post')
        super(ScriptsForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        inst = super(ScriptsForm, self).save(commit=False)
        inst.author = self._user
        inst.post_id = self.post
        if commit:
            inst.save()
            self.save_m2m()
        return inst


class FeedbackForm(ModelForm):
    class Meta:
        model = Feedback
        fields = ('body',)

        widgets = {
            'title': Textarea(attrs={'class': 'form-control', 'cols': 20, 'rows': 1}),
            'body': Textarea(attrs={'class': 'form-control', 'cols': 20, 'rows': 10}),
        }

    def __init__(self, *args, **kwargs):
        self._user = kwargs.pop('user')
        super(FeedbackForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        inst = super(FeedbackForm, self).save(commit=False)
        inst.author = self._user
        if commit:
            inst.save()
            self.save_m2m()
        return inst


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = UsernameField(widget=TextInput(
        attrs={'class': 'form-control', 'cols': 2, 'rows': 1}
    ))
    password = CharField(widget=PasswordInput(
        attrs={'class': 'form-control', 'cols': 2, 'rows': 1}
    ))

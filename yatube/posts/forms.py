from django.forms import ModelForm, Select, Textarea

from .models import Post


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group')


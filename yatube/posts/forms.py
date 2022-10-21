from django.forms import ModelForm, Textarea, Select
from .models import Post



class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group')
        widgets = {
                "text" : Textarea(attrs = {
                "cols" : "40",
                "rows" : "10",
                "class" : "form-control",
                "placeholder" : "Введите текст",
            }),
                "group" : Select(attrs = {
                "class" : "form-control",
                "id" : "id_group",

            }),
        }



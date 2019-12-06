from django import forms
from .models import Post

class CreatePost(forms.ModelForm):

    class Meta:
        model = Post
        fields = ("title", "content", "status")
        labels ={
            "title": "Titulo",
            "content" : "Contenido",
            "status" : "Estatus"
        }

    def __init__(self, *args, **kwargs):
        super(CreatePost, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
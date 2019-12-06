from django import forms
from .models import Post

class CreatePost(forms.ModelForm):

    class Meta:
        model = Post
        fields = ("title", "content", "status")

    def __init__(self, *args, **kwargs):
        super(CreatePost, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
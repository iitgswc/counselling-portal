from django import forms

from .models import post

class post_form(forms.ModelForm):
    class Meta:
        model = post
        fields = {
            "title",
            "content",
            "option"
        }

        def __init__(self, *args, **kwargs):
            super(post_form, self).__init__(*args, **kwargs)
            self.fields.keyOrder = ['content', 'option','title']
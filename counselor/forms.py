from django import forms

from .models import message, reply

class mess_to_couns(forms.ModelForm):
    class Meta:
        model = message
        fields = {

            "content",
            "title",
        }
        field_order =["title","content"]


class reply_form(forms.ModelForm):
    class Meta:
        model = reply
        fields = {
            "content"
        }
from .models import Category, Comment
from django import forms


class CreateCommentForm(forms.Form):
    class Meta:
        model = Category
        field = (
            'content',
        )
        Widget = {
            'content': forms.TextInput(attrs={'id': 'input-comment'})
        }

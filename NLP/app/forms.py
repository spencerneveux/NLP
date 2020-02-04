from django import forms


class ArticleForm(forms.Form):
    name = forms.CharField(max_length=100)
    content = forms.CharField(widget=forms.Textarea)

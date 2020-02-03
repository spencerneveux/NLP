from django import forms


class AuthorForm(forms.Form):
    author_name = forms.CharField(label="author name", max_length=100)

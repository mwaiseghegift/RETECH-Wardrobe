from django import forms
from .models import Profile


class ResetEmailForm(forms.Form):
    email = forms.EmailField()

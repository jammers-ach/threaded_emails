
from django.forms.models import ModelForm
from django import forms
from bootstrap_form.forms import BootstrapForm


class EmailForm(BootstrapForm):
    to  = forms.EmailField()
    email_text = forms.CharField(widget=forms.Textarea())


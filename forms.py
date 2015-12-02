
from django.forms.models import ModelForm
from django import forms
from bootstrap_form.forms import BootstrapForm,BootstrapModelForm
from .models import EmailTemplateCategory,EmailTemplate

class EmailForm(BootstrapForm):
    to  = forms.CharField()
    email_subject =  forms.CharField()
    email_text = forms.CharField(widget=forms.Textarea())


class EmailTemplateCategoryForm(BootstrapModelForm):
    class Meta:
        model = EmailTemplateCategory
        exclude = []


class EmailTemplateForm(BootstrapModelForm):
    class Meta:
        model = EmailTemplate
        exclude =[]

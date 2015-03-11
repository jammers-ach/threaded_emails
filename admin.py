from django.contrib import admin
from models import MailBox,EmailMessage,EmailTemplate,EmailTemplateCategory

admin.site.register(MailBox)
admin.site.register(EmailMessage)
admin.site.register(EmailTemplate)
admin.site.register(EmailTemplateCategory)
# Register your models here.

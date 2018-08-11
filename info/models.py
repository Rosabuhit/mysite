from django.db import models
from django.utils import timezone
from django import forms
from ckeditor_uploader.fields import RichTextUploadingField

class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    sender = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)
    copy = forms.BooleanField(required=False)


class News(models.Model):
    title = models.CharField(max_length=200)
    body = RichTextUploadingField(blank=True, default='')
    created_date = models.DateTimeField(
        default=timezone.now)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return "/page/%i/" % self.id
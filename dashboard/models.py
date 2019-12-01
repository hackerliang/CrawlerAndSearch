from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField


class News(models.Model):
    title = models.CharField(max_length=500, null=False, blank=True)
    author = models.CharField(max_length=100, null=False, blank=True)
    url = models.URLField(max_length=500, null=False, blank=True)
    content = RichTextUploadingField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.title

    def __str__(self):
        return "%s <%s>" % (self.title, self.author)

from django.db import models
from django import forms
from django.utils import timezone
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.utils.text import slugify


class CBSRequestLog(models.Model):
    REQ_TYPES = (
       ("outgoing", "outgoing"),
       ("incoming", "incoming"),
    )
    REQ_TYPES_MAP = dict(REQ_TYPES)

    REQ_METHODS = (
       ("get", "get"),
       ("post", "post"),
       ("put", "put"),
       ("delete", "delete"),
    )
    REQ_METHODS_MAP = dict(REQ_METHODS)

    url = models.CharField(max_length=2000)
    request_id = models.CharField(max_length=256)
    method = models.CharField(choices=REQ_METHODS,max_length=28)
    direction = models.CharField(choices=REQ_TYPES,max_length=28)
    request_headers = models.CharField(max_length=2000)
    request_data = models.CharField(max_length=7000)
    response_headers = models.CharField(max_length=2000)
    response_content = models.TextField(default='')
    response_http_status = models.IntegerField()
    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField()

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(CBSRequestLog, self).save(*args, **kwargs)
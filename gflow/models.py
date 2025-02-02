from django.db import models
from django import forms
from django.utils import timezone
from app.models import User
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.utils.text import slugify


class GFlowPage(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200, default='', blank=True)
    content = models.TextField(default='<html></html>')
    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField()

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        self.slugify_name()
        return super(GFlowPage, self).save(*args, **kwargs)

    def slugify_name(self):
        self.name = slugify(self.name)

    def delete(self):
        super(GFlowPage, self).delete()

    def __str__(self):
        return self.name + '__' + str(self.id)

class GFlowCollection(models.Model):
    name = models.CharField(max_length=100)
    pages = models.ManyToManyField(GFlowPage)
    description = models.CharField(max_length=200, default='', blank=True)
    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(GFlowCollection, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class GFlowApp(models.Model):
    ACCESS_CHANNELS = (
       ("private", "private"),
       ("public", "public"),
       ("all", "all"),
    )
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    routing = models.SlugField(max_length=100)
    published = models.BooleanField(default=False)
    channel = models.CharField(choices=ACCESS_CHANNELS,max_length=28)
    collections = models.ManyToManyField(GFlowCollection,blank=True, default=None)
    pages = models.ManyToManyField(GFlowPage,blank=True, default=None)
    description = models.CharField(max_length=200, default='', blank=True)
    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField(default=timezone.now)

    # def create_permission(self):
    #     content_type = ContentType.objects.get_for_model(GFlowCollection)
    #     code_names = []
    #     code_names.append([f'access_{self.slug}', f"Can Access App '{self.slug}'"])
    #     code_names.append([f'create_{self.slug}', f"Can Crate in App '{self.slug}'"])
    #     code_names.append([f'edit_{self.slug}', f"Can Edit in App '{self.slug}'"])
    #     code_names.append([f'delete_{self.slug}', f"Can Delete in App '{self.slug}'"])
    #     for codename in code_names:
    #         if Permission.objects.filter(codename=codename[0]).count() < 1:
    #             permission = Permission.objects.create(
    #                 codename = codename[0],
    #                 name = codename[1],
    #                 content_type=content_type,)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
            # self.create_permission()
        self.modified = timezone.now()
        return super(GFlowApp, self).save(*args, **kwargs)

class GFlowPageUserStates(models.Model):
    customer_user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    current_page = models.CharField(max_length=100)


# @receiver(post_delete, sender=GFlowApp)
# def delete_permission_hook(sender, instance, using, **kwargs):
#     codename = f'access_{instance.name}'
#     permission = Permission.objects.filter(codename=codename)
#     if permission.count() > 0:
#         permission.delete()
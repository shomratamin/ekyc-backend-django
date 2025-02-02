from django.db import models
from django.template.defaultfilters import slugify

class Bank(models.Model):
    name = models.CharField(max_length=255,default='None')
    slug = models.SlugField(unique=True, max_length=255)
    test_quota = models.IntegerField(default=100)
    live_quota = models.IntegerField(default=100)
    is_default = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True, editable=False)
    updated_on = models.DateTimeField(auto_now=True)
    REQUIRED_FIELDS = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Bank, self).save(*args, **kwargs)
    


    class Meta:
        ordering = ['created_on']

        def __unicode__(self):
            return self.name

        def __str__(self):
            return self.name


from django.db import models
from .bank import Bank
from django.utils import timezone

class EcStatus(models.Model):
    average_ec_response = models.IntegerField(default=-1)
    ec_server_status = models.CharField(max_length=50,default='unchecked')
    is_set_ec_credentials = models.BooleanField(default=False)
    is_ec_logged_in = models.BooleanField(default=False)
    is_ec_credentials_valid = models.CharField(max_length=50,default='unchecked')
    up_time = models.IntegerField(default=0)
    nid_info_req_queue = models.IntegerField(default=0)
    nid_info_upstream_queue = models.IntegerField(default=0)
    upstream_status_queue = models.IntegerField(default=0)
    ec_job_running = models.BooleanField(default=False)
    upstream_job_running = models.BooleanField(default=False)
    agent_status = models.CharField(max_length=50, default='unchecked')
    last_checked = models.DateTimeField()

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        self.last_checked = timezone.now()
        return super(EcStatus, self).save(*args, **kwargs)
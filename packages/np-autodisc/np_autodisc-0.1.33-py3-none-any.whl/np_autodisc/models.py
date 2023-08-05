from django.db import models
from django.urls import reverse
from django_rq import get_queue
from rq import cancel_job

from dcim.models import Device, DeviceRole, Platform, Site
from ipam.fields import IPAddressField, IPNetworkField
from np_autodisc.np_transitions.models import ChangeLoggedModel

from np_autodisc.constants import *

class DiscoveryRequest(ChangeLoggedModel):
    prefix = IPNetworkField()
    update_existing = models.BooleanField(
        default = False
    )
    status = models.PositiveSmallIntegerField(
        choices = REQUEST_STATUS_CHOICES,
        default = REQUEST_STATUS_PENDING
    )
    platform = models.ForeignKey(
        to = Platform,
        related_name = '+',
        on_delete = models.CASCADE
    )
    job = models.CharField(
        max_length = 50,
        null = True,
        blank = True
    )
    site = models.ForeignKey(
        to = Site,
        related_name = '+',
        on_delete = models.CASCADE
    )
    device_role = models.ForeignKey(
        to = DeviceRole,
        related_name = '+',
        on_delete = models.CASCADE
    )

    def __str__(self):
        return f'{self.prefix} {self.created}'

    def get_absolute_url(self):
        return reverse('np_autodisc:discoveryrequest', args=[self.pk])

    def get_status_class(self):
        return REQUEST_STATUS_CLASSES[self.status]

    def save(self, *args, **kwargs):
        new = True
        if self.pk:
            new = False
        
        super().save(*args, **kwargs)

        if new:
            discovery_queue = get_queue('default')
            job = discovery_queue.enqueue(
                "np_autodisc.worker.discovery_job",
                self
            )
            self.job = str(job.key)
            self.save()

    def delete(self, *args, **kwargs):
        if self.job:
            try:
                cancel_job(self.job)
            except Exception:
                pass
        super().delete(*args, **kwargs)

class DiscoveryResult(models.Model):
    discovery_request = models.ForeignKey(
        to = DiscoveryRequest,
        related_name = 'results',
        on_delete = models.CASCADE
    )
    device = models.ForeignKey(
        to = Device,
        related_name = '+',
        null = True,
        blank = True,
        on_delete = models.SET_NULL,
    )
    address = IPAddressField()
    status = models.PositiveSmallIntegerField(
        choices = RESULT_STATUS_CHOICES,
        default = RESULT_STATUS_TRYING
    )

    def __str__(self):
        return f'{self.address} {self.status}'

    def get_absolute_url(self):
        return reverse('np_autodisc:discoveryresult', args = [self.pk])

    def get_status_class(self):
        return RESULT_STATUS_CLASSES[self.status]

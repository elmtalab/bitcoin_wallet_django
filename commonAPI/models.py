from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

# Create your models here.

class BTCAddresses(models.Model):
    address = models.CharField(max_length=50, primary_key=True)
    created = models.DateTimeField(default=now)
    isUsed  = models.BooleanField(default=False)
    user_id = models.IntegerField(blank=True, null=True, default=None)
    label   = models.CharField(max_length=50, blank=True, null=True, default=None)
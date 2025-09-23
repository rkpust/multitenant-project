from django.db import models
import uuid
from django.utils import timezone
from datetime import timedelta

# Create your models here.
from django.db import models

class Tenant(models.Model):
    name = models.CharField(max_length=255)
    domain = models.URLField()

    def __str__(self):
        return self.name

class Invitation(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('ACCEPTED', 'Accepted'),
        ('EXPIRED', 'Expired'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    tenant = models.ForeignKey('Tenant', on_delete=models.CASCADE)  # assuming a Tenant model exists
    name = models.CharField(max_length=255)
    email = models.EmailField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    expiration_date = models.DateTimeField(null=True,)
    metadata = models.JSONField(null=True, blank=True)  # For IP address or notes

    def set_expiration(self):
        self.expiration_date = timezone.now() + timedelta(days=7)

    def __str__(self):
        return f"Invitation for {self.email} - {self.status}"

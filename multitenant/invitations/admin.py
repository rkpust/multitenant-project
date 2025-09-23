from django.contrib import admin
from .models import Tenant, Invitation

# Register your models here.
admin.site.register(Tenant)
admin.site.register(Invitation)
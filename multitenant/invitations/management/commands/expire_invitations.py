from django.core.management.base import BaseCommand
from django.utils import timezone
from invitations.models import Invitation

class Command(BaseCommand):
    help = 'Mark invitations expired if the expiration date has passed.'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        expired_invitations = Invitation.objects.filter(expiration_date__lt=now, status='PENDING')
        
        for invitation in expired_invitations:
            invitation.status = 'EXPIRED'
            invitation.save()
            self.stdout.write(self.style.SUCCESS(f'Expired invitation for {invitation.email}'))

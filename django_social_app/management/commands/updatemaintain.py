#update remain time
from django.core.management.base import BaseCommand, CommandError
from django_social_app.models import maintain_schedule
from django.utils import timezone
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    #def add_arguments(self, parser):
        #parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        maintain_schedule.updateTimeRemainning()


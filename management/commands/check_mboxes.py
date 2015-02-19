from django.core.management.base import BaseCommand, CommandError
from threaded_emails.checker import check_all_mailboxes

class Command(BaseCommand):
    args = ''
    help = 'checks all the mailboxes if they need checked'

    def handle(self, *args, **options):
        check_all_mailboxes()

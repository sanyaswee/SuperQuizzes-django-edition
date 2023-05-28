from django.core.management import BaseCommand
from home.models import Completion


class Command(BaseCommand):
    help = 'Drop all statistics (Completion and UserAnswer objects)'

    def handle(self, *args, **options):
        print('You are going to clear all statistics. This will delete all "Completion" and "UserAnswer" objects')
        answer = input('Are you sure? ("yes" to continue): ')
        if answer == 'yes':
            Completion.objects.all().delete()
            print('Statistics are now clean')
        else:
            print('Operation canceled')

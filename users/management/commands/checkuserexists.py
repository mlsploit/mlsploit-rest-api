import sys

from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand

from users.models import User


class Command(BaseCommand):
    help = "Throws error if user does not exists"

    def add_arguments(self, parser):
        parser.add_argument("username", type=str, help="Username to be checked")

    def handle(self, *args, **kwargs):
        username = kwargs["username"]

        try:
            User.objects.get(username=username)
        except ObjectDoesNotExist:
            sys.exit(1)
        else:
            sys.exit(0)

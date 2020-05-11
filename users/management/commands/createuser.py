import sys

from django.core.management.base import BaseCommand

from users.models import User


class Command(BaseCommand):
    help = "Creates a new user account"

    def add_arguments(self, parser):
        parser.add_argument(
            "-u",
            "--username",
            type=str,
            default="testuser",
            help="Username to be created",
        )

        parser.add_argument(
            "-p",
            "--password",
            type=str,
            default="testpassword",
            help="Password for the account",
        )

    def handle(self, *args, **kwargs):
        username = kwargs["username"]
        password = kwargs["password"]

        try:
            user = User.objects.create(username=username)
            user.set_password(password)
            user.save()
        except Exception:
            sys.exit(1)
        else:
            print("Created user %s with ID %s" % (username, user.id))
            sys.exit(0)

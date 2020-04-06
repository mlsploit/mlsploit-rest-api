from django.core.management.base import BaseCommand

from modules.models import Module


class Command(BaseCommand):
    help = "Remove a module"

    def add_arguments(self, parser):
        parser.add_argument("name", type=str, help="Name of the module to be deleted")

    def handle(self, *args, **kwargs):
        name = kwargs["name"]

        m = Module.objects.get(name=name)
        m.delete()

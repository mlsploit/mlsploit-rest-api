import glob
import json
import os
import shutil
import tempfile

from django.core.management.base import BaseCommand
from git import Git

from modules.models import Module


class Command(BaseCommand):
    help = "Creates a new module"

    def add_arguments(self, parser):
        parser.add_argument("name", type=str, help="Name of the module to be created")
        parser.add_argument(
            "repo", type=str, help="Link to git repository containing the module"
        )

    def handle(self, *args, **kwargs):
        name = kwargs["name"]
        repo = kwargs["repo"]

        assert repo.endswith(".git"), '"repo" should end with .git'

        tmp_dir = tempfile.mkdtemp()

        try:
            Git(tmp_dir).clone(repo)
            repo_dir = glob.glob(os.path.join(tmp_dir, "*"))[0]

            input_schema = open(os.path.join(repo_dir, "input.schema"), "r").read()
            output_schema = open(os.path.join(repo_dir, "output.schema"), "r").read()

            input_schema_dict = json.loads(input_schema)
            doctxt = input_schema_dict.get("doctxt", "")
            tagline = input_schema_dict.get("tagline", "")

            Module.objects.create(
                name=name,
                repo=repo,
                doctxt=doctxt,
                tagline=tagline,
                input_schema=input_schema,
                output_schema=output_schema,
            )

        except Exception as e:
            print(f"[ERROR] {e}")

        shutil.rmtree(tmp_dir)

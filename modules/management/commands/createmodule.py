import glob
import json
import os
import shutil
import tempfile

from django.core.management.base import BaseCommand
from git import Git

from mlsploit import Module as ModuleConfig
from mlsploit.paths import ModulePaths

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

        Git(tmp_dir).clone(repo)
        repo_dir = glob.glob(os.path.join(tmp_dir, "*"))[0]

        ModulePaths.set_module_dir(repo_dir)
        module_config = ModuleConfig.load()

        Module.objects.create(
            name=name,
            repo=repo,
            display_name=module_config.display_name,
            tagline=module_config.tagline,
            doctxt=module_config.doctxt,
            config=module_config.serialize(),
            icon_url=module_config.icon_url or "",
        )

        shutil.rmtree(tmp_dir)

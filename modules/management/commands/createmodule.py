import glob
import json
import os
import shutil
import tempfile

from django.core.management.base import BaseCommand
import git

from mlsploit import Module as ModuleConfig
from mlsploit.paths import ModulePaths

from modules.models import Module


class Command(BaseCommand):
    help = "Creates a new module"

    def add_arguments(self, parser):
        parser.add_argument("name", type=str, help="Name of the module to be created")
        parser.add_argument(
            "repo_url", type=str, help="Link to git repository containing the module"
        )
        parser.add_argument(
            "-b", "--branch", type=str, default="master", help="Branch to be cloned"
        )

    def handle(self, *args, **kwargs):
        name = kwargs["name"]
        repo_url = kwargs["repo_url"]
        repo_branch = kwargs["branch"]

        assert repo_url.endswith(".git"), '"repo_url" should end with .git'

        repo_dir = tempfile.mkdtemp()

        print(f"Cloning branch {repo_branch} from {repo_url}...")
        git.Repo.clone_from(repo_url, repo_dir, branch=repo_branch)

        ModulePaths.set_module_dir(repo_dir)
        module_config = ModuleConfig.load()

        Module.objects.create(
            name=name,
            repo_url=repo_url,
            repo_branch=repo_branch,
            display_name=module_config.display_name,
            tagline=module_config.tagline,
            doctxt=module_config.doctxt,
            config=module_config.serialize(),
            icon_url=module_config.icon_url or "",
        )

        shutil.rmtree(repo_dir)

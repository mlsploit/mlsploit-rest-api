from enum import Enum
from hashlib import md5
import json
import os
import random
from string import ascii_lowercase

from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver

from api.settings import MEDIA_DIR
from users.models import User


def make_upload_path(instance, filename):
    directory_hash = "".join(random.choice(ascii_lowercase) for _ in range(8))

    return os.path.join(MEDIA_DIR, "files", directory_hash, filename)


class File(models.Model):
    class FileKind(Enum):
        INPUT = "INPUT"
        OUTPUT = "OUTPUT"

        @classmethod
        def choices(cls):
            return tuple((i.name, i.value) for i in cls)

    name = models.CharField(max_length=100, editable=False)
    owner = models.ForeignKey(User, related_name="files", on_delete=models.CASCADE)
    blob = models.FileField(upload_to=make_upload_path, null=False)
    kind = models.CharField(
        max_length=100,
        choices=FileKind.choices(),
        default=FileKind.INPUT.value,
        blank=False,
    )
    tags = models.TextField(default="{}")
    parent_file = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, related_name="modified_versions"
    )
    date_uploaded = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return f"{self.__class__.__name__}[{self.name}]"

    def save(self, *args, **kwargs):
        filename = os.path.basename(self.blob.name)
        self.name = filename
        self.tags = json.dumps(json.loads(self.tags))
        super(File, self).save(*args, **kwargs)


@receiver(post_delete, sender=File)
def delete_file_from_storage(sender, instance, **kwargs):
    # TODO: delete parent directory if empty
    instance.blob.delete(False)

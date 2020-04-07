import json

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from mlsploit import Module as ModuleConfig
from mlsploit.core.module import Option as OptionConfig, Tag as TagConfig


class Module(models.Model):
    name = models.CharField(max_length=25, unique=True)
    repo_url = models.CharField(max_length=200, unique=True)
    repo_branch = models.CharField(max_length=50, default="master")
    display_name = models.CharField(max_length=25, unique=True)
    tagline = models.CharField(max_length=50)
    doctxt = models.TextField()
    config = models.TextField()
    icon_url = models.TextField(blank=True)

    def __str__(self):
        return f"{self.__class__.__name__}[{self.name}]"

    def save(self, *args, **kwargs):
        valid_config = ModuleConfig.deserialize(self.config)
        self.config = valid_config.serialize()
        super(Module, self).save(*args, **kwargs)


class Function(models.Model):
    name = models.CharField(max_length=25, unique=True)
    module = models.ForeignKey(
        Module, related_name="functions", on_delete=models.CASCADE
    )
    doctxt = models.TextField()
    options = models.TextField()
    creates_new_files = models.BooleanField(null=False)
    modifies_input_files = models.BooleanField(null=False)
    expected_filetype = models.CharField(max_length=10)
    optional_filetypes = models.TextField(default="[]")
    output_tags = models.TextField(default="[]")

    def __str__(self):
        return f"{self.__class__.__name__}[{self.name}]"

    def save(self, *args, **kwargs):
        raw_options = json.loads(self.options)
        valid_options = map(lambda d: OptionConfig(**d), raw_options)
        valid_options = map(lambda o: o.dict(), valid_options)
        self.options = json.dumps(list(valid_options))

        raw_tags = json.loads(self.output_tags)
        valid_tags = map(lambda d: TagConfig(**d), raw_tags)
        valid_tags = map(lambda t: t.dict(), valid_tags)
        self.output_tags = json.dumps(list(valid_tags))

        self.optional_filetypes = json.dumps(json.loads(self.optional_filetypes))

        super(Function, self).save(*args, **kwargs)


@receiver(post_save, sender=Module)
def create_functions(sender, instance, **kwargs):
    module = instance

    module_config = ModuleConfig.deserialize(module.config)

    for fn in module_config.functions:
        Function.objects.create(
            name=fn.name,
            module=module,
            doctxt=fn.doctxt,
            options=json.dumps(list(map(lambda o: o.dict(), fn.options))),
            creates_new_files=fn.creates_new_files,
            modifies_input_files=fn.modifies_input_files,
            expected_filetype=fn.expected_filetype,
            optional_filetypes=json.dumps(fn.optional_filetypes),
            output_tags=json.dumps(list(map(lambda t: t.dict(), fn.output_tags))),
        )

import json

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Module(models.Model):
    name = models.CharField(max_length=100, unique=True)
    repo = models.CharField(max_length=200, unique=True, blank=False, null=False)
    doctxt = models.TextField(default='')
    tagline = models.TextField(default='')
    input_schema = models.TextField(default='{}')
    output_schema = models.TextField(default='{}')

    def __str__(self):
        return f'{self.__class__.__name__}[{self.name}]'

    def save(self, *args, **kwargs):
        self.input_schema = json.dumps(json.loads(self.input_schema))
        self.output_schema = json.dumps(json.loads(self.output_schema))
        super(Module, self).save(*args, **kwargs)


class Function(models.Model):
    name = models.CharField(max_length=100, unique=True)
    module = models.ForeignKey(Module, related_name='functions',
                               on_delete=models.CASCADE)
    doctxt = models.TextField(default='')
    options = models.TextField(default='[]')

    def __str__(self):
        return f'{self.__class__.__name__}[{self.name}]'

    def save(self, *args, **kwargs):
        self.options = json.dumps(json.loads(self.options))
        super(Function, self).save(*args, **kwargs)


@receiver(post_save, sender=Module)
def create_functions(sender, instance, **kwargs):
    module = instance

    input_schema = json.loads(module.input_schema)

    for fn in input_schema['functions']:
        Function.objects.create(
            name=fn['name'],
            module=module,
            doctxt=fn.get('doctxt', ''),
            options=json.dumps(fn.get('options', [])))

import json
from enum import Enum

from django.db import models
from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver

from files.models import File
from modules.models import Function
from users.models import User


class Pipeline(models.Model):
    name = models.CharField(blank=False, max_length=100)
    owner = models.ForeignKey(
        User, related_name="pipelines", on_delete=models.CASCADE, editable=False
    )
    enabled = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return f"{self.__class__.__name__}[{self.name}]"


class Task(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    pipeline = models.ForeignKey(
        Pipeline, blank=False, related_name="tasks", on_delete=models.CASCADE
    )
    function = models.ForeignKey(
        Function, blank=False, null=True, on_delete=models.SET_NULL
    )
    arguments = models.TextField(default="{}", blank=False, null=False)
    order = models.IntegerField(default=1, editable=False)
    date_created = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        ordering = ("order",)

    def __str__(self):
        return f"{self.__class__.__name__}[{self.function.name}]"

    def save(self, *args, **kwargs):
        order = self.pipeline.tasks.count() + 1
        self.order = order
        self.arguments = json.dumps(json.loads(self.arguments))
        super(Task, self).save(*args, **kwargs)


class Run(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    pipeline = models.ForeignKey(
        Pipeline, blank=False, related_name="runs", on_delete=models.CASCADE
    )
    files = models.ManyToManyField(File, blank=False)
    date_created = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return f"{self.__class__.__name__}[{self.pipeline.name}]"


class Job(models.Model):
    class JobStatus(Enum):
        PENDING = "PENDING"
        QUEUED = "QUEUED"
        RUNNING = "RUNNING"
        FAILED = "FAILED"
        FINISHED = "FINISHED"

        @classmethod
        def choices(cls):
            return tuple((i.name, i.value) for i in cls)

    owner = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    run = models.ForeignKey(
        Run, blank=False, related_name="jobs", on_delete=models.CASCADE
    )
    task = models.ForeignKey(Task, blank=False, on_delete=models.CASCADE)
    parent_job = models.ForeignKey("self", on_delete=models.CASCADE, null=True)
    status = models.CharField(
        max_length=100,
        choices=JobStatus.choices(),
        default=JobStatus.PENDING.value,
        blank=False,
    )
    output = models.TextField(blank=True, null=True)
    output_files = models.ManyToManyField(File, blank=True)
    logs = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, editable=False)

    def save(self, *args, **kwargs):
        if self.output is not None:
            self.output = json.dumps(json.loads(self.output))
        super(Job, self).save(*args, **kwargs)


@receiver(post_save, sender=Run)
def create_jobs(sender, instance, **kwargs):
    run = instance
    owner = run.owner
    tasks = run.pipeline.tasks.all()
    parent_job = None

    for task in tasks:
        parent_job = Job.objects.create(
            owner=owner, task=task, run=run, parent_job=parent_job
        )


@receiver(pre_delete, sender=Job)
def delete_output_files(sender, instance, **kwargs):
    job = instance
    output_files = job.output_files.all()
    for output_file in output_files:
        output_file.delete()

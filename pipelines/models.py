# pipelines/models.py
from django.db import models
from core.models import User
from contacts.models import Contact


class Pipeline(models.Model):
    PIPELINE_TYPE_CHOICES = [
        ('SALES', 'Verkauf'),
        ('RECRUITMENT', 'Rekrutierung'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pipelines')
    name = models.CharField(max_length=100)
    pipeline_type = models.CharField(max_length=20, choices=PIPELINE_TYPE_CHOICES)

    def __str__(self):
        return self.name


class Stage(models.Model):
    pipeline = models.ForeignKey(Pipeline, on_delete=models.CASCADE, related_name='stages')
    name = models.CharField(max_length=100)
    order = models.IntegerField()

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


class PipelineContact(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='pipeline_stages')
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE, related_name='contacts')
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.contact} - {self.stage}"
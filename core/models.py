# core/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_premium = models.BooleanField(default=False)


class Tag(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='tags')

    def __str__(self):
        return self.name


# contacts/models.py
from django.db import models
from core.models import User, Tag


class Contact(models.Model):
    CONTACT_TYPE_CHOICES = [
        ('CUSTOMER', 'Kunde'),
        ('POTENTIAL_CUSTOMER', 'Potenzieller Kunde'),
        ('PARTNER', 'Partner'),
        ('POTENTIAL_PARTNER', 'Potenzieller Partner'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contacts')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    contact_type = models.CharField(max_length=20, choices=CONTACT_TYPE_CHOICES)
    tags = models.ManyToManyField(Tag, related_name='contacts', blank=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    lead_score = models.IntegerField(default=0)  # Für KI-Lead-Scoring

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Policy(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='policies')
    name = models.CharField(max_length=100)
    policy_type = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.contact}"


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


# teams/models.py
from django.db import models
from core.models import User


class TeamMember(models.Model):
    upline = models.ForeignKey(User, on_delete=models.CASCADE, related_name='downline')
    downline = models.ForeignKey(User, on_delete=models.CASCADE, related_name='upline')
    level = models.IntegerField(default=1)  # Direkte Partner = 1, deren Partner = 2, usw.

    class Meta:
        unique_together = ('upline', 'downline')

    def __str__(self):
        return f"{self.upline.username} -> {self.downline.username}"


# Für Follow-Up-System
class Task(models.Model):
    TASK_TYPE_CHOICES = [
        ('CALL', 'Anruf'),
        ('EMAIL', 'E-Mail'),
        ('MEETING', 'Treffen'),
        ('OTHER', 'Sonstiges'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    contact = models.ForeignKey('contacts.Contact', on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    task_type = models.CharField(max_length=20, choices=TASK_TYPE_CHOICES)
    due_date = models.DateTimeField()
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
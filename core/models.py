# core/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_premium = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class Tag(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='tags')

    def __str__(self):
        return self.name


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
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
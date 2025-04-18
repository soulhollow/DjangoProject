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
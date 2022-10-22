from django.conf import settings
from django.db import models
from django.urls import reverse


class Partie(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    nazwa = models.CharField(max_length=100)
    PGN = models.TextField(blank=True)
    FEN = models.TextField(blank=True)

    def __str__(self):
        return self.nazwa

    def get_absolute_url(self):  # new
        return reverse(args=[str(self.id)])

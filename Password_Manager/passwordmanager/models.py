from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Account(models.Model):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=100, blank=True)
    password = models.CharField(max_length=100)
    link = models.URLField(max_length=100, blank=True, null=True)
    notes = models.TextField(blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ('author', 'name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('account-detail', kwargs={'pk': self.pk})

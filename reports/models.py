from django.db import models
from profiles.models import Profile


class Report(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='reports', blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)
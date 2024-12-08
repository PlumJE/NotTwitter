from django.db import models

# Create your models here.
class Posts(models.Model):
    id = models.TextField(primary_key=True, blank=True)
    writer = models.TextField(default='', blank=True)
    writedate = models.TextField(default='', blank=True)
    content = models.TextField(default='', blank=True)

    class Meta:
        managed = True
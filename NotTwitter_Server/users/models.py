from django.db import models

# Create your models here.
class UserDetails(models.Model):
    id = models.TextField(primary_key=True, blank=True)
    birth = models.DateField(default='', blank=True)
    phone = models.TextField(default='', blank=True)
    families = models.TextField(default='', blank=True)
    nation = models.TextField(default='', blank=True)
    legion = models.TextField(default='', blank=True)
    job = models.TextField(default='', blank=True)
    jobaddr = models.TextField(default='', blank=True)

    class Meta:
        managed = True
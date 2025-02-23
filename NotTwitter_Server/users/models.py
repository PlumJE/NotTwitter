from django.db import models

# Create your models here.
class UserDetails(models.Model):
    id = models.IntegerField(primary_key=True, blank=True)
    birth = models.DateField(default='1000-01-01', blank=True)
    phone = models.TextField(default='010-0000-0000', blank=True)
    families = models.TextField(default='', blank=True)
    nation = models.TextField(default='Earth', blank=True)
    legion = models.TextField(default='Earth', blank=True)
    job = models.TextField(default='', blank=True)
    jobaddr = models.TextField(default='', blank=True)
    profileimg = models.ImageField(upload_to='images/profiles/', default='', blank=True)

    class Meta:
        managed = True
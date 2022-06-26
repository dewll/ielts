from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    username = models.CharField(max_length = 20,default = '', blank=True, null = True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length = 20)
    zip_code = models.CharField(max_length = 20)
    score = models.IntegerField(null = True, blank=True)
    state = models.CharField(max_length = 150)
    city = models.CharField(max_length = 150)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [ 'username','first_name', 'last_name',
                       'phone','zip_code','score',
                       'state','city']

class Audio_store(models.Model):
    record = models.FileField(upload_to='audios/')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,default = '1',
                                on_delete = models.CASCADE, null = True)
    
    def __str__(self):
        return (f"{self.owner.first_name} {self.owner.last_name} record")
    class Meta:
        db_table='Audio_store'
        
class Skill(models.Model):
    package = models.CharField(max_length = 150,blank = True, null=True)
    amount = models.CharField(max_length = 150,blank = True, null=True)
    user_skill = models.ForeignKey(settings.AUTH_USER_MODEL,default = '1',
                                on_delete = models.CASCADE, null = True)
    
    def __str__(self):
        return self.package
        
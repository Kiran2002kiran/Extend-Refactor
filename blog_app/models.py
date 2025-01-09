from django.db import models
from django.contrib.auth.models import AbstractUser
from general.models import Country , Address
from general.models import AbstractCommonModel
# Create your models here.



class User(AbstractUser):
    date_of_birth = models.DateField(null=True , blank=True)
    bio = models.TextField(null=True , blank=True)
    country = models.ForeignKey(Country , on_delete=models.SET_NULL , null=True , blank=True)
    address = models.OneToOneField(Address , null=True , blank=True , on_delete=models.SET_NULL )

    def __str__(self):
        return self.username

class Blog(AbstractCommonModel):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_by = models.ForeignKey(User , on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.title} by {self.created_by.username}"


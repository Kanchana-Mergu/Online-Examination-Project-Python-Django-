from django.db import models
from django.contrib.auth.models import User
from django.db.models.base import Model

# Create your models here.
class Teacher(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic=models.ImageField(upload_to='profile_pic/Teacher/',null=True,blank=True)
    mobile=models.CharField(max_length=20,null=False)
    status=models.BooleanField(default=True)

    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    

    
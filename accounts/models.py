from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.



User_role={
     "Guest":"Guest", 
    "student":"student",
    "instructor":"instructor",
    "admin":"admin"
}
    


class CustomUser(AbstractUser):
      role=models.CharField(max_length=10, choices=User_role, default="Guest")
      phone=models.CharField(max_length=15, blank=True, null=True)
      
      def __str__(self):
            return self.username 
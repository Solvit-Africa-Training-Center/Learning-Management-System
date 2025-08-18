from django.db import models
from django.contrib.auth.models import AbstractUser
import string
from django.utils import timezone
import random

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

      otp=models.CharField(max_length=6, blank=True, null=True)
      otp_expiry=models.DateTimeField(blank=True, null=True)
      is_verified=models.BooleanField(default=False)

      
          
      def __str__(self):
            return self.username 
      
      def generate_otp(self):
            self.otp=''.join(random.choices(string.digits, k=6))
            self.otp_expiry=timezone.now() + timezone.timedelta(minutes=10)
            self.save(update_fields=['otp', 'otp_expiry'])
            return self.otp
      def verify_otp(self, otp):
            if self.otp == otp and self.otp_expiry > timezone.now():
                  return True
            else:
                  return False
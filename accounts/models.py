from django.db import models
from django.contrib.auth.models import AbstractUser, User


# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     age = models.IntegerField(null=True, blank=True)

#     def __str__(self):
#         return f"{self.user.username} Profile"


class UserProfile(AbstractUser):
    age = models.PositiveIntegerField(null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    # picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"
        
    def __str__(self):
        return self.username
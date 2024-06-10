from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, name, password=None, interests=None):
        if not name:
            raise ValueError('Users must have a name')

        user = self.model(
            name=name,
            interests=interests or [],
        )

        user.set_password(password)  
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    name = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=128)  
    interests = models.JSONField(default=list)

    objects = UserManager()

    USERNAME_FIELD = 'name'

    def __str__(self):
        return self.name
    

class Group(models.Model):
    users = models.ManyToManyField(User)
    group_name = models.CharField(max_length=100)

    def __str__(self):
        return self.group_name

from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)
    # interests = models.TextField()
    interests = models.JSONField(default=list)

    def __str__(self):
        return self.name
    

class Group(models.Model):
    users = models.ManyToManyField(User)
    group_name = models.CharField(max_length=100)

    def __str__(self):
        return self.group_name

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class Gossip(models.Model):
    title = models.TextField()
    content=models.TextField()
    author = models.ForeignKey(User, 
                               on_delete=models.CASCADE, 
                               related_name="gossips")
class Comment(models.Model):
    gossip = models.ForeignKey(Gossip,
                               on_delete=models.CASCADE,
                               related_name="comments",)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments"
    )

    content = models.TextField()

# Create your models here.

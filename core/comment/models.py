from django.db import models

# Create your models here.
from core.abstract.models import AbstractModel, AbstractManager

class CommentManager(AbstractManager):
    pass 

class Comment(AbstractModel):
    post = models.ForeignKey("core_post.Post", on_delete=models.PROTECT)
    author = models.ForeignKey("core_user.User", on_delete=models.PROTECT)
    body = models.TextField() 
    edited = models.BooleanField(default=False)

    object = CommentManager() 

    def __str__(self):
        return self.author.name  
    
    
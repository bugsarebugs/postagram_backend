from django.db import models
import uuid 
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ObjectDoesNotExist 
from django.http import Http404 
from core.abstract.models import AbstractManager, AbstractModel 

class UserManager(BaseUserManager, AbstractManager):
    def get_object_by_public_id(self, public_id):
        try:
            instance = self.get(public_id=public_id)
            return instance  
        except (ObjectDoesNotExist, ValueError, TypeError):
            return Http404 
    
    def create_user(self, username, email, password=None, **kwargs):
        """ Create and return a `User` with an email, phone number, username and password."""
        if username is None:
            raise TypeError('Users must have a username.')
        if email is None:
            raise TypeError("Users must have a an email.")
        if password is None:
            raise TypeError("Users must have a password.")
    

        user = self.model(username=username, email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.save(using=self._db)

        return user  

    def create_superuser(self, username, email, password, **kwargs):
        """ Create and return a `User` with superuser (admin) permissions. """
        if password is None:
            raise TypeError('Superusers must have a password. ')
        if email is None:
            raise TypeError("Superusers must have an email.")
        if username is None:
            raise TypeError("Superusers must have an username.")
        
        user = self.create_user(username, email, password, **kwargs)
        user.is_superuser = True 
        user.is_staff = True  
        user.save(using=self._db)

        return user  
    
def user_directory_path(instance, filename):
    # File will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.public_id, filename)

# Create your models here.
class User(AbstractModel, AbstractBaseUser, PermissionsMixin):
    public_id = models.UUIDField(db_index=True, unique=True, default=uuid.uuid4, editable=False)
    username = models.CharField(db_index=True, max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(db_index=True, unique=True)
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to=user_directory_path, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)
    #for user like 
    posts_liked = models.ManyToManyField("core_post.Post", related_name="liked_by")
    comments_liked = models.ManyToManyField("core_comment.Comment", related_name="commented_by")
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager() 

    def like_post(self, post):
        """ Like `post` if it hasn't been done yet"""
        return self.posts_liked.add(post)
    
    def remove_like_post(self, post):
        """ Remove a like from a `post`"""
        return self.posts_liked.remove(post)
    
    def has_liked_post(self, post):
        """ Return True if the User has liked a `post` ; else False"""
        return self.posts_liked.filter(pk=post.pk).exists()

    def like_comment(self, comment):
        """ Like `Comment` if it has not been done yet"""
        return self.comments_liked.add(comment)
    
    def remove_like(self, comment):
        """ Remove a Like from a comment"""
        return self.comments_liked.remove(comment)
    
    def has_liked_comment(self, comment):
        """ Return True if the user has liked a comment; else False"""
        return self.comments_liked.filter(pk=comment.pk).exists()

   
    def __str__(self):
        return f"{self.email}"
    
    @property 
    def name(self):
        return f"{self.first_name} {self.last_name}"
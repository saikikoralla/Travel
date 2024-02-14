from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
    
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('The Email field must be set')
        if not password:
            raise ValueError('The Password field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None):
        if not email:
            raise ValueError('The Email field must be set')
        if not password:
            raise ValueError('The Password field must be set')
        user=self.create_user(email, password)
        user.is_superuser=True
        user.is_staff=True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)  # Add the is_superuser field
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS=[]
    objects = CustomUserManager()

    def __str__(self):
        usertype=('Admin' if self.is_superuser else 'User')
        return f'{usertype} : {self.profile_obj.first_name}'
    class Meta:
        ordering=['is_superuser']

def profile_image_path(instance, filename):
    return f'profiles_images/{instance.username.email}/{filename}'

class Profile(models.Model):
    username=models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True,related_name='profile_obj')
    first_name=models.CharField(max_length=24,null=True,blank=True)
    last_name=models.CharField(max_length=24,null=True,blank=True)
    phone_no=models.CharField(max_length=10,null=True,blank=True,validators=[RegexValidator(regex='\d{10}', message='Phone number must be 10 digits long.')])
    address=models.CharField(max_length=255,null=True,blank=True)
    Img=models.ImageField(gettext_lazy("Image"),upload_to=profile_image_path, default='profile_images/default.jpg')
    

    def __str__(self):
        return f'{self.first_name} : {self.username.email}'

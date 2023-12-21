from django.db import models

#to create a custom user model and to use it in admin panel
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _

#to automatically create one to one object of user model
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class MyUserManager(BaseUserManager):
    """ A custom user manager to deal with emails as unique identifiers for auth"""	
    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password"""
        if not email:
            raise ValueError("The Email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email,password,**extra_fields):
        """Create and save a SuperUser with the given email and password"""
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_active',True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True")
        return self._create_user(email,password,**extra_fields)

class User(AbstractBaseUser,PermissionsMixin):
    """A custom user model that uses email as unique identifier for auth"""
    email = models.EmailField(_("email address"),unique=True, null = False)
    is_staff = models.BooleanField(_("staff status"),
    default=False,
    help_text= _("Designates whether the user can log into this admin site.")
    )

    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text = _(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )

    objects = MyUserManager()

    USERNAME_FIELD = 'email'

    def get_full_name(self):
        """The user is identified by their email address"""
        return self.email

    def get_short_name(self):
        """The user is identified by their email address"""
        return self.email

    def __str__(self):
        return self.email

class Profile(models.Model):
    """A profile model for a user"""
    user = models.OneToOneField(User,on_delete=models.CASCADE, related_name="profile")
    username = models.CharField(max_length=264,blank=True)
    full_name = models.CharField(max_length=264,blank=True)
    address_1 = models.CharField(max_length=300,blank=True)
    city = models.CharField(max_length=40,blank=True)
    zipcode = models.CharField(max_length=10,blank=True)
    country = models.CharField(max_length=40,blank=True)
    phone = models.CharField(max_length=20,blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username + "'s profile"

    def is_fully_filled(self):
        """Method to check if all the fields are filled"""
        fields_names = [f.name for f in self._meta.get_fields()]

        for field_name in fields_names:
            value = getattr(self,field_name)
            if value is None or value == "":
                return False
        return True

@receiver(post_save,sender=User)
def create_profile(sender,instance,created,**kwargs):
    """A signal to create a profile when a user is created"""
    if created:
        #if created then automatically create a profile object
        Profile.objects.create(user=instance)

@receiver(post_save,sender=User)
def save_profile(sender,instance,**kwargs):
    """A signal to save a profile when a user is saved"""
    instance.profile.save()
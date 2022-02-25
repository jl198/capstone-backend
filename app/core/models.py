from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.postgres.fields import ArrayField, HStoreField


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        if email is False:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Creates and saves a new super user"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class GameManager:

    def create_game(self):
        pass


class Game(LoginRequiredMixin):
    """Game model belonging to specific user"""
    creator_id = models.ForeignKey('user.id', null=False,
                                   on_delete=models.CASCADE())
    created_date = models.DateTimeField(auto_now_add=True)
    date_played = models.DateTimeField(blank=True, null=True)
    num_players = models.IntegerField(blank=False, null=False)
    occupied_stations = HStoreField(keys=('1', '2', '3', '4', '5', ),
                                    blank=False, null=False, default=False)
    starting_station =




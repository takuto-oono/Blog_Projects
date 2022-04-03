from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from django.contrib.auth.validators import UnicodeUsernameValidator


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError('usernameを入力してください')
        username = self.model.normalize_username(username)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('is_staff=Trueである必要があります。')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('is_superuser=Trueである必要があります。')
        return self._create_user(username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        verbose_name='アカウント名', max_length=50, validators=[UnicodeUsernameValidator()], unique=True)
    is_staff = models.BooleanField(verbose_name='管理者権限', default=False)
    is_active = models.BooleanField(verbose_name='ログイン状況', default=True)
    date_joined = models.DateTimeField(
        verbose_name='アカウント作成日', default=timezone.now)
    objects = UserManager()
    USERNAME_FIELD = 'username'

    class Meta:
        verbose_name_plural = 'アカウント'

    def clean(self):
        super().clean()

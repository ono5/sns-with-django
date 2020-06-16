from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_field):

        if not email:
            raise ValueError('email is must')

        user = self.model(email=self.normalize_email(email), **extra_field)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email


def upload_path(instance, filename):
    # 拡張子を取り出す
    ext = filename.split('.')[-1]
    return '/'.join(['image', str(instance.user_pro.id) + str(instance.nick_name) + str('.') + str(ext)])


class Profile(models.Model):
    nick_name = models.CharField(max_length=20)
    user_pro = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name='user_pro',
        on_delete=models.CASCADE,
    )
    created_on = models.DateTimeField(auto_now_add=True)
    img = models.ImageField(blank=True, null=True, upload_to=upload_path)

    def __str__(self):
        return self.nick_name


class FriendRequest(models.Model):
    ask_from = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='ask_from',
        on_delete=models.CASCADE,
    )

    ask_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='ask_to',
        on_delete=models.CASCADE,
    )
    approved = models.BooleanField(default=False)

    class Meta:
        # 申請は1回のみに限定
        unique_together = (('ask_from', 'ask_to'),)

    def __str__(self):
        return str(self.ask_from) + '--------->' + str(self.ask_to)


class Message(models.Model):
    message = models.CharField(max_length=140)
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='sender',
        on_delete=models.CASCADE,
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='receiver',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.sender


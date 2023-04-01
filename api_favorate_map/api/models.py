from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings

# Create your models here.

"""
BaseUserManagerをオーバーライド
username,password => email,password
"""


class UserManager(BaseUserManager):

    def create_user(self, email, password=None) -> object:
        if not email:
            raise ValueError('email is must')

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password) -> object:
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


"""
Userテーブル定義
ユーザー情報テーブル
"""


class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'  # デフォルトだとusernameになってる

    def __str__(self) -> str:
        return self.email


"""
Profileテーブル定義
プロフィールデータテーブル
---------------------------
One to one (User=>Profile)
"""


class Profile(models.Model):

    nickName = models.CharField(max_length=20)
    userProfile = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name='userProfile',
        on_delete=models.CASCADE
    )
    created_on = models.DateTimeField(auto_now_add=True)
    img = models.ImageField(
        blank=True,
        null=True,
        upload_to=upload_avatar_path
    )

    def __str__(self) -> str:
        return self.nickName

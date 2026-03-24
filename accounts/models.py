from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, mail, phone, password=None):
        if not mail:
            raise ValueError("El usuario debe tener un correo electrónico")
        if not username:
            raise ValueError("El usuario debe tener un nombre de usuario")
        
        user = self.model(
            mail=self.normalize_email(mail),
            username=username,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
        )
        
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, first_name, last_name, username, mail, phone=None, password=None):
        user = self.create_user(
            mail=self.normalize_email(mail),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user



class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    mail = models.EmailField(max_length=250, unique=True)
    phone = models.CharField(max_length=50)

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'mail'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'phone']

    objects = MyAccountManager()
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.mail

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

 
class userProfile(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    address_line_1 = models.CharField(blank=True, max_length=100)
    address_line_2 = models.CharField(blank=True, max_length=100)
    profile_picture = models.ImageField(blank=True, upload_to='userprofile')
    city = models.CharField(blank=True, max_length=20)
    state = models.CharField(blank=True, max_length=20)
    country = models.CharField(blank=True, max_length=20)

    def __str__(self):
        return self.user.first_name
    
    def full_address(self):
        return f'{self.address_line_1} {self.address_line_2}'
    
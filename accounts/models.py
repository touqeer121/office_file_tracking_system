from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.core.validators import RegexValidator
from django.urls import reverse
from django.contrib.auth.password_validation import validate_password
from django.template.defaultfilters import slugify
from django.utils.text import slugify


class Department(models.Model):
    name = models.CharField(max_length=255, default='')
    slug = models.SlugField(max_length=30, unique=True, editable=False)
    abbreviation = models.CharField(max_length=10, default='')
    # courses_provided = models.CharField(max_length=10, default='')

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = slugify(self.name)
            while True:
                try:
                    department = Department.objects.get(slug=slug)
                    if department == self:
                        self.slug = slug
                        break
                    else:
                        slug = slug + '_'
                except:
                    self.slug = slug
                    break
        super(Department, self).save()

    def __str__(self):
        return self.name


class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, email=None):
        if not username:
            raise ValueError('Users must have a username')
        user = self.model(
            username=username + '',
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        user = self.create_user(
            username=username,
            password=password,
        )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    GENDERS = (('M', 'Male'), ('F', 'Female'))
    ROLE_CHOICES = (
        ('Teacher', 'Teacher'),
        ('Faculty Advisor', 'Faculty Advisor'),
        ('Dean', 'Dean'),
        ('Head of department', 'Head of department'),
        ('Admin', 'Admin'),
    )
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    mobile = models.CharField(max_length=10,
                              validators=[RegexValidator(regex=r'[0-9]{10}', message='Invalid Mobile Number')],
                              blank=True)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='S')
    gender = models.CharField(max_length=1, choices=GENDERS, default='M')

    registration_number = models.CharField('Registration number', max_length=7, unique=True,
                                           validators=[RegexValidator(regex=r'[a-zA-Z]{2}[0-9]{5}',
                                            message='Invalid Registration Number')], blank=True, null=True)

    department = models.ForeignKey('Department', verbose_name="Department", on_delete=models.CASCADE, blank=True, null=True)

    admin = models.CharField(max_length=1, default='N')
    password = models.CharField('password', max_length=128, validators=[validate_password])
    is_student = models.BooleanField(default=True, verbose_name='Student')
    is_active = models.BooleanField(default=False, verbose_name='Active',
                                    help_text='Designates whether this user should be treated as active. '
                                              'Unselect this instead of deleting accounts.')
    is_admin = models.BooleanField(default=False, verbose_name='Staff status',
                                   help_text='Designates whether the user can log into this admin site.')
    image = models.ImageField(default='download.jpg', upload_to='profile/')
    # notifications = models.IntegerField(default=0)
    # noti_messages = models.CharField(max_length=500, blank=True)
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'

    objects = CustomUserManager()

    def __str__(self):
        return self.username

    @property
    def is_staff(self):
        return self.is_admin

    def get_absolute_url(self):
        return reverse('accounts:index')


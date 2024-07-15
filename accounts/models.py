import uuid
from django.db import models
from base.choices import UserType
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.contrib.auth.models import AbstractUser, UserManager


class BaseModel(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CustomUserManager(UserManager):
    def _create_user(self, mobile_number, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        user = self.model(mobile_number=mobile_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, mobile_number=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(mobile_number, password, **extra_fields)

    def create_superuser(self, mobile_number, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(mobile_number, password, **extra_fields)


class CustomUser(AbstractUser):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    username = None
    email = models.EmailField(null=True, blank=True, unique=True)
    first_name = models.CharField(max_length=250, blank=True)
    last_name = models.CharField(max_length=250, blank=True)
    mobile_number = models.CharField(max_length=50,
                                     error_messages={"unique": "A user with this phone number already exists"},
                                     unique=True,
                                     db_index=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    user_type = models.CharField(max_length=10, choices=UserType.get_choices())
    city = models.CharField(max_length=150, null=True, blank=True)
    postcode = models.CharField(max_length=150, null=True, blank=True)
    country = models.CharField(max_length=150, null=True, blank=True)



    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()


    class Meta:
        ordering = ('first_name', 'mobile_number')
        verbose_name_plural = 'Users'
        verbose_name = 'User'


class CustomerProfile(BaseModel):
    id = None
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True,
                                limit_choices_to={'user_type': UserType.customer.value[0]},
                                related_name='customer_profile')
    delivery_address = models.PointField(default=Point())

    class Meta:
        ordering = ('user__first_name',)


class RiderProfile(BaseModel):
    id = None
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True,
                                limit_choices_to={'user_type': UserType.rider.value[0]},
                                related_name='rider_profile')
    current_location = models.PointField(default=Point())
    on_delivery = models.BooleanField(default=False,)

    class Meta:
        ordering = ('user__first_name',)


class RestaurantProfile(BaseModel):
    id = None
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True,
                                limit_choices_to={'user_type': UserType.restaurant.value[0]},
                                related_name='restaurant_profile')
    location = models.PointField(default=Point())

    class Meta:
        ordering = ('user__first_name',)


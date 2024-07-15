from django.db import models
from base.choices import UserType
from base.base_upload_handlers import handle_menu_file
from order_service.choices import StatusType
from accounts.models import CustomUser, BaseModel


class MenuItem(BaseModel):
    restaurant = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                                   limit_choices_to={'user_type': UserType.restaurant.value[0]})
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to=handle_menu_file, null=True, blank=True)
    is_non_veg = models.BooleanField()
    price = models.PositiveIntegerField()

    class Meta:
        ordering = ('name',)


class Order(BaseModel):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'user_type': UserType.customer.value[0]})
    items = models.ManyToManyField(MenuItem)
    total_price = models.PositiveIntegerField(null=True, blank=True)
    driver = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='order_driver',
                               limit_choices_to={'user_type': UserType.rider.value[0]})
    status = models.CharField(max_length=10, choices=StatusType.get_choices(), default=StatusType.in_progress.value[0])

    class Meta:
        ordering = ('-created_at',)


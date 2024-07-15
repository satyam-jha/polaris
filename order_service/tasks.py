from order_service.models import Order
from accounts.models import CustomUser
from base.choices import UserType
from django.contrib.gis.db.models.functions import Distance


def assign_rider(order_id):
    order = Order.objects.get(id=order_id)
    riders = CustomUser.objects.filter(user_type=UserType.rider.value[0], on_delivery=False).annotate(distance=Distance(
                'rider_profile__current_location', order.items.first().restaurant.restaurant_profile.location)).order_by('distance')
    if riders.exists():
        driver = riders.first()
        order.driver = driver
        order.save(update_fields=['driver'])
        driver.on_delivery = True
        driver.save(update_fields=['on_delivery'])

    return 'Driver assigned'
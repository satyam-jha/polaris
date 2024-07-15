from base.choices import UserType, StatusType
from order_service.tasks import assign_rider
from django.db.models import Sum
from rest_framework import serializers
from order_service.choices import StatusType
from order_service.models import MenuItem, Order
from accounts.serializers import CustomUserSerializer, CustomGeometryField


class MenuItemSerializer(serializers.ModelSerializer):
    restaurant = CustomUserSerializer(read_only=True)

    class Meta:
        model = MenuItem
        fields = (
            'id',
            'restaurant',
            'name',
            'description',
            'image',
            'is_non_veg',
            'price'
        )

    def create(self, validated_data):
        request = self.context['request']
        validated_data.update({
            'restaurant': request.user,
        })
        instance = super().create(validated_data)
        return instance


class OrderSerializer(serializers.ModelSerializer):
    customer = CustomUserSerializer(read_only=True)
    driver = CustomUserSerializer(read_only=True)
    items = MenuItemSerializer(read_only=True, many=True)


    class Meta:
        model = Order
        fields = (
            'id',
            'customer',
            'items',
            'total_price',
            'driver',
            'status',
        )

    def create(self, validated_data):
        request = self.context['request']
        items = MenuItem.objects.filter(id__in=request.data.getlist('item_ids'))
        validated_data.update({
            'customer': request.user,
            'total_price': items.aggregate(Sum('price'))['price__sum'],
            'items': items
        })
        instance = super().create(validated_data)
        return instance

    def update(self, instance, validated_data):
        request = self.context['request']
        if request.user_type == UserType.restaurant.value[0] and request.data.get('status') == StatusType.accepted.value[0]:
            assign_rider(instance.id)

        if request.user_type == UserType.rider.value[0] and request.data.get('status') == StatusType.delivered.value[0]:
            instance.driver.on_delivery = False
            instance.driver.save(update_fields=['on_delivery'])

        instance = super().update(instance, validated_data)
        return instance

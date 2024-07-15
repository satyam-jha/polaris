from rest_framework import serializers
from base.choices import UserType
from accounts.models import CustomUser, RestaurantProfile, RiderProfile, CustomerProfile
from django.contrib.gis.geos import Point
from rest_framework_gis.fields import GeometryField
from rest_framework.validators import UniqueValidator
from django.contrib.auth.hashers import make_password


class CustomPasswordField(serializers.CharField):
    def __init__(self, **kwargs):
        self.required = False
        super().__init__(**kwargs)

    def to_internal_value(self, data):
        data = make_password(data)
        return super().to_internal_value(data)


class CustomEmailField(serializers.EmailField):
    #To Standardize the email platform, so we won't get Satyam@gmail.com and satyam@gmail.com as two different emails

    def to_internal_value(self, data):
        data = data.lower()
        return super().to_internal_value(data)


class CustomGeometryField(GeometryField):
    def to_representation(self, value):
        if isinstance(value, Point):
            if not value.coords:
                return None
        return super().to_representation(value)


class CustomerProfileSerializer(serializers.ModelSerializer):
    delivery_address = CustomGeometryField(required=False)

    class Meta:
        model = CustomerProfile
        fields = (
            'delivery_address',
        )


class RiderProfileSerializer(serializers.ModelSerializer):
    current_location = CustomGeometryField(required=False)

    class Meta:
        model = RiderProfile
        fields = (
            'current_location',
            'on_delivery',
        )


class RestaurantProfileSerializer(serializers.ModelSerializer):
    location = CustomGeometryField(required=False)

    class Meta:
        model = RestaurantProfile
        fields = (
            'location',
        )


class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=100, required=False)
    email = CustomEmailField(
        max_length=254,
        required=False
    )
    password = CustomPasswordField()

    class Meta:
        model = CustomUser
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'password',
            'mobile_number',
            'address',
            'city',
            'user_type',
            'postcode',
            'country',
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.pop('password')
        if instance.user_type == UserType.customer.value[0]:
            data['customer_profile'] = CustomerProfileSerializer(
                instance.customer_profile, context=self.context).data
        if instance.user_type == UserType.rider.value[0]:
            data['rider_profile'] = RiderProfileSerializer(
                instance.rider_profile, context=self.context).data
        if instance.user_type == UserType.restaurant.value[0]:
            data['restaurant_profile'] = RestaurantProfileSerializer(
                instance.restaurant_profile, context=self.context).data
        return data

    def create(self, validated_data):
        instance = super().create(validated_data)
        if instance.user_type == UserType.customer.value[0]:
            customer_profile_serializer = CustomerProfileSerializer(
                data=self.initial_data, context=self.context)
            customer_profile_serializer.is_valid(raise_exception=True)
            customer_profile_serializer.save(user=instance)
        if instance.user_type == UserType.rider.value[0]:
            rider_profile_serializer = RiderProfileSerializer(
                data=self.initial_data, context=self.context)
            rider_profile_serializer.is_valid(raise_exception=True)
            rider_profile_serializer.save(user=instance)
        if instance.user_type == UserType.restaurant.value[0]:
            restaurant_profile_serializer = RestaurantProfileSerializer(
                data=self.initial_data, context=self.context)
            restaurant_profile_serializer.is_valid(raise_exception=True)
            restaurant_profile_serializer.save(user=instance)
        return instance

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        if instance.user_type == UserType.customer.value[0]:
            customer_profile_serializer = CustomerProfileSerializer(
                instance=instance.customer_profile, data=self.initial_data,
                context=self.context, partial=True)
            customer_profile_serializer.is_valid(raise_exception=True)
            customer_profile_serializer.save()
        if instance.user_type == UserType.rider.value[0]:
            rider_profile_serializer = RiderProfileSerializer(
                dinstance=instance.customer_profile, data=self.initial_data,
                context=self.context, partial=True)
            rider_profile_serializer.is_valid(raise_exception=True)
            rider_profile_serializer.save(user=instance)
        if instance.user_type == UserType.restaurant.value[0]:
            restaurant_profile_serializer = RestaurantProfileSerializer(
                instance=instance.customer_profile, data=self.initial_data,
                context=self.context, partial=True)
            restaurant_profile_serializer.is_valid(raise_exception=True)
            restaurant_profile_serializer.save(user=instance)
        return instance
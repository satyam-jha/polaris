from order_service.serializers import MenuItemSerializer, OrderSerializer
from order_service.models import MenuItem, Order
from base.choices import UserType
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, UpdateModelMixin
from strings import *



class MenuItemBaseView(GenericAPIView, ListModelMixin, CreateModelMixin):
    queryset = MenuItem.objects.select_related('restaurant')
    serializer_class = MenuItemSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(restaurant_id=self.request.query_params.get('restaurant_id'))
        return qs

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class MenuItemDetailView(MenuItemBaseView, UpdateModelMixin):

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class OrderBaseAPIView(GenericAPIView, ListModelMixin, CreateModelMixin):
    queryset = Order.objects.all().select_related('customer').prefetch_related('items')
    serializer_class = OrderSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.user_type == UserType.rider.value[0]:
            qs = qs.filter(driver_id=self.request.user.id)
        else:
            qs = qs.filter(customer_id=self.request.user.id)
        return qs

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class OrderDetailView(MenuItemBaseView, UpdateModelMixin):

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)




from django.db import transaction
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action

from service.models import Restaurent, Branch, FoodItem, Order, OrderDiscription
from service.serializers import FoodItemSerializer, RestaurentSerializer, BranchSerializer, OrderSerializers, \
    OrderDiscriptionSerializers


class RestaurentViewSet(viewsets.ModelViewSet):
    queryset = Restaurent.objects.all().prefetch_related('branches')
    serializer_class = RestaurentSerializer


class BranchViewSet(viewsets.ModelViewSet):
    serializer_class = BranchSerializer

    def get_queryset(self):
        restaurent = self.kwargs['restaurent_pk']
        try:
            int(restaurent)
            return Branch.objects.filter(restaurent_id=self.kwargs['restaurent_pk'])
        except ValueError:
            return Branch.objects.filter(restaurent_id=None)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['restaurent'] = self.kwargs['restaurent_pk']
        return context

    @action(detail=True, methods=['POST'])
    @transaction.atomic
    def placeOrder(self, request, pk, restaurent_pk):
        data = request.data
        data["user"] = request.user
        data['branch'] = self.kwargs['pk']
        serializer = OrderSerializers(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response("Order Placed", status=status.HTTP_200_OK)


class FoodItemViewSet(viewsets.ModelViewSet):
    serializer_class = FoodItemSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['branch'] = self.kwargs['branch_pk']
        return context

    def get_queryset(self):
        branch = self.kwargs['branch_pk']
        restaurent = self.kwargs['restaurent_pk']
        try:
            int(branch)
            int(restaurent)
            return FoodItem.objects.filter(branch_id=self.kwargs['branch_pk'])
        except ValueError:
            return FoodItem.objects.filter(branch_id=None)



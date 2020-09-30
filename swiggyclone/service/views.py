from django.db import transaction
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from service.models import Restaurent, Branch, FoodItem
from service.serializers import FoodItemSerializer, RestaurentSerializer, BranchSerializer, OrderSerializers


class RestaurentViewSet(viewsets.ModelViewSet):
    queryset = Restaurent.objects.all().prefetch_related('branches')
    serializer_class = RestaurentSerializer


class BranchViewSet(viewsets.ModelViewSet):
    serializer_class = BranchSerializer

    def get_queryset(self):
        restaurent = self.kwargs['restaurent_pk']
        return Branch.objects.filter(restaurent_id=self.kwargs['restaurent_pk'])

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['restaurent'] = self.kwargs['restaurent_pk']
        return context

    @action(detail=True, methods=['POST'])
    @transaction.atomic
    def place_order(self, request, pk, restaurent_pk):
        data = request.data
        data["user"] = request.user.id
        data['branch'] = self.kwargs['pk']
        try:
            with transaction.atomic():
                serializer = OrderSerializers(data=data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response("Order Placed", status=status.HTTP_200_OK)
        except Exception as exception:
            return Response({'result': 'Order failed, please try again.'},
                            status=status.HTTP_422_UNPROCESSABLE_ENTITY)



class FoodItemViewSet(viewsets.ModelViewSet):
    serializer_class = FoodItemSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['branch'] = self.kwargs['branch_pk']
        return context

    def get_queryset(self):
        branch = self.kwargs['branch_pk']
        restaurent = self.kwargs['restaurent_pk']
        return FoodItem.objects.filter(branch_id=self.kwargs['branch_pk'])

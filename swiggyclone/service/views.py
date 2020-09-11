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
        return Branch.objects.filter(restaurent_id=self.kwargs['restaurent_pk'])

    def perform_create(self, serializer):
        serializer.save(restaurent_id=self.kwargs['restaurent_pk'])

    @action(detail=True, methods=['POST'])
    def placeOrder(self, request, pk, restaurent_pk):
        data = request.data
        data["user"] = request.user
        data['branch'] = self.kwargs['pk']
        serializer = OrderSerializers(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response("Order Placed", status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FoodItemViewSet(viewsets.ModelViewSet):
    serializer_class = FoodItemSerializer

    def get_queryset(self):
        return FoodItem.objects.filter(branch_id=self.kwargs['branch_pk'])

    def perform_create(self, serializer):
        serializer.save(branch_id=self.kwargs['branch_pk'])

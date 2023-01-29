from django.shortcuts import render
# Create your views here.
from customer.models import Customer, Products
from customer.serializers import CustomerSerializer, ProductSerializer
from rest_framework.response import Response
from rest_framework import viewsets, status
from datetime import datetime

activateExc = {
    'error': "Your product can not be inactivate before 2 months.",
    'status_code': status.HTTP_400_BAD_REQUEST
}


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer

    def retrieve(self, request, *args, **kwargs):
        params = kwargs
        print(params['pk'])

        products = Products.objects.filter(name=params['pk'])
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        productsData = request.data

        activateApprovement, dateOfregister = self.ProductActivationApprovement(
            productsData["activate_IND"], productsData["register_date"])
        if (activateApprovement == False):
            return Response(data=activateExc)

        new_Prod = Products.objects.create(customer_id=Customer.objects.get(id=productsData["customer_id"]),
                                           name=productsData["name"],
                                           registerKey=productsData["registerKey"],
                                           activate_IND=productsData["activate_IND"],
                                           register_date=dateOfregister)

        new_Prod.save()
        serializer = ProductSerializer(new_Prod)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        productObj = self.get_object()
        productsData = request.data

        activateApprovement, dateOfregister = self.ProductActivationApprovement(
            productsData["activate_IND"], productsData["register_date"])
        if (activateApprovement == False):
            return Response(data=activateExc)

        productObj.customer_id = Customer.objects.get(
            id=productsData["customer_id"])
        productObj.name = productsData["name"]
        productObj.registerKey = productsData["registerKey"]
        productObj.activate_IND = productsData["activate_IND"]
        productObj.register_date = dateOfregister

        productObj.save()

        serializer = ProductSerializer(productObj)

        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        instance = self.get_object()
        if not instance:
            return Response(status=status.HTTP_404_NOT_FOUND)

        productsData = request.data
        activateApprovement,dateOfregister = self.ProductActivationApprovement(
            productsData["activate_IND"], instance.register_date)
        if (activateApprovement == False):
            return Response(data=activateExc)

        serializer = self.get_serializer(instance,
                                         data=request.data,
                                         many=isinstance(request.data, list),
                                         partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()  # NOT WORKING; NEEDS ARGS instance, validated_data
        return Response(serializer.data, status=status.HTTP_200_OK)

    def ProductActivationApprovement(self, activate_IND, dateOfregister):
        if type(dateOfregister) != datetime:
            dateOfregister = datetime.strptime(
                dateOfregister, '%Y/%m/%d %H:%M:%S')

        if (activate_IND):
            return True, dateOfregister

        tdelta = datetime.now()-dateOfregister.replace(tzinfo=None)
        return tdelta.days > 30, dateOfregister

from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework.decorators import api_view
from rest_framework import status
from .models import MenuItem, Cart, OrderItem, Order
from .serializers import MenuItemSerializer, UserSerializer, GroupSerializer, CartSerializer, OrderItemSerializer, OrderSerializer
from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404


@api_view(["GET", "POST", "PUT", "PATCH", "DELETE"])
@permission_classes([IsAuthenticated])
def MenuItemView(request):

    if request.method == "GET":
        items = MenuItem.objects.all()
        serialized_item = MenuItemSerializer(items, many=True)
        return Response(serialized_item.data, status=status.HTTP_200_OK)

    if request.user.groups.filter(name="Manager").exists() or request.user.groups.filter(name="Admin").exists():
        if request.method == "POST":
            serializer = MenuItemSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if request.method == "DELETE":
            return Response(status=status.HTTP_200_OK)
        if request.method == "PATCH":
            return Response(status=status.HTTP_200_OK)  # ojo estas
        if request.method == "PUT":
            return Response(status=status.HTTP_200_OK)

    else:
        return Response({"message": " Unauthorized"}, 403)


@api_view(["GET", "POST", "PUT", "PATCH", "DELETE"])
@permission_classes([IsAuthenticated])
def SingleMenuItemView(request, pk):
    if request.method == "GET":
        try:
            items = MenuItem.objects.get(id=pk)
        except MenuItem.DoesNotExist:
            return Response({"message": "item does not exist"}, status=status.HTTP_404_NOT_FOUND)
        serialized_item = MenuItemSerializer(items)
        return Response(serialized_item.data, status=status.HTTP_200_OK)

    if request.user.groups.filter(name="Manager").exists():
        if request.method == "POST":
            serializer = MenuItemSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if request.method == "DELETE":
            try:
                objeto = MenuItem.objects.get(id=pk)
            except MenuItem.DoesNotExist:
                return Response({"message": "item does not exist"}, status=status.HTTP_404_NOT_FOUND)
            objeto.delete()
            return Response({"message": "Object deleted."}, status=status.HTTP_200_OK)
        if request.method == "PATCH":
            try:
                objeto = MenuItem.objects.get(id=pk)
            except MenuItem.DoesNotExist:
                return Response({"message": "item does not exist"}, status=status.HTTP_404_NOT_FOUND)
            serializer = MenuItemSerializer(
                objeto, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == "PUT":
            try:
                objeto = MenuItem.objects.get(id=pk)
            except MenuItem.DoesNotExist:
                return Response({"message": "item does not exist"}, status=status.HTTP_404_NOT_FOUND)
            serializer = MenuItemSerializer(objeto, data=request.data)
            if serializer.is_valid():
                serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({"message": " Unauthorized"}, 403)


@api_view(["POST", "GET", "DELETE"])
@permission_classes([IsAuthenticated])
def managers(request):
    if request.user.groups.filter(name="Manager").exists() or request.user.groups.filter(name="Admin").exists() :
        if request.method == "GET":
            queryset = User.objects.filter(groups="1")
            serializer = UserSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        else:

            username = request.data["username"]
            if username:
                user = get_object_or_404(User, username=username)
                managers = Group.objects.get(name="Manager")

                if request.method == "POST":
                    managers.user_set.add(user)
                return Response({"message": "ok"}, status.HTTP_201_CREATED)
            return Response({"message": "bad request"}, status.HTTP_400_BAD_REQUEST)
    return Response({"message": " Unauthorized"}, 403)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def managers_remove(request, pk):
    if request.user.groups.filter(name="Manager").exists():
        user = get_object_or_404(User, id=pk)
        managers = Group.objects.get(name="Manager")
        if request.method == "DELETE":
            managers.user_set.remove(user)
            return Response({"message": "ok"}, status.HTTP_200_OK)

    return Response({"message": " Unauthorized"}, 403)


@api_view(["POST", "GET", "DELETE"])
@permission_classes([IsAuthenticated])
def delivery(request):
    if request.user.groups.filter(name="Manager").exists():
        if request.method == "GET":
            queryset = User.objects.filter(groups="2")
            serializer = UserSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        else:

            username = request.data["username"]
            if username:
                user = get_object_or_404(User, username=username)
                managers = Group.objects.get(name="Delivery crew")

                if request.method == "POST":
                    managers.user_set.add(user)
                return Response({"message": "ok"}, status.HTTP_200_OK)
            return Response({"message": "bad request"}, status.HTTP_400_BAD_REQUEST)
    return Response({"message": " Unauthorized"}, 403)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delivery_remove(request, pk):
    if request.user.groups.filter(name="Manager").exists():
        user = get_object_or_404(User, id=pk)
        managers = Group.objects.get(name="Delivery crew")
        if request.method == "DELETE":
            managers.user_set.remove(user)
            return Response({"message": "ok"}, status.HTTP_200_OK)
    return Response({"message": " Unauthorized"}, 403)


@api_view(["POST", "GET", "DELETE"])
@permission_classes([IsAuthenticated])
def customer(request):
    if request.method == "GET":
        user = request.user
        queryset = Cart.objects.filter(user=user)
        serializer = CartSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    if request.method == "POST":
        user = request.user.id
        menuitem = request.data.get("menuitem", "")
        quantity = request.data.get("quantity", "")
        unit_price = request.data.get("unit_price", "")
        price = request.data.get("price", "")

        queryset = CartSerializer(data={
            'quantity': quantity,
            'unit_price': unit_price,
            'price': price,
            'user': user,
            'menuitem': menuitem
        })
        if queryset.is_valid():
            queryset.save()
            return Response({"message": "ok"}, status.HTTP_201_CREATED)
        return Response(queryset.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "DELETE":
        user = request.user
        obj = Cart.objects.filter(user=user)
        obj.delete()
        return Response({"message": "Object deleted."}, status=status.HTTP_200_OK)


@api_view(["POST", "GET"])
@permission_classes([IsAuthenticated])
def OrderView(request):
    if request.method == "GET":
        
        if request.user.groups.filter(name="Manager").exists():
            queryset_two = OrderItem.objects.all()
            serializer_two = OrderItemSerializer(queryset_two, many=True)
            return Response(serializer_two.data, status=status.HTTP_200_OK)
        if request.user.groups.filter(name="Delivery crew").exists():
            user = request.user
            objeto = Order.objects.filter(delivery_crew=user)
            objeto_serialized = OrderSerializer(objeto, many = True)
            return Response(objeto_serialized.data, status=status.HTTP_200_OK)
            
        else:
            user = request.user
            queryset_two = OrderItem.objects.filter(order=user)
            serializer_two = OrderItemSerializer(queryset_two, many=True)
            return Response(serializer_two.data, status=status.HTTP_200_OK)
    
    if request.method == "POST":
        user = request.user
        objeto = Cart.objects.filter(user=user)
        
        #order_objeto = {"order":objeto.user.id,"menuitem":objeto.menuitem.id,"quantity":objeto.quantity.id,"unit_price":objeto.unit_price.id,"price":objeto.unit_price.id}
        objeto_serialized = OrderItemSerializer (data=objeto, many=True)
        
        if objeto_serialized.is_valid():
            objeto_serialized.save()
            objeto.delete()
        # return Response(objeto_serialized.data, status.HTTP_200_OK)
        return Response({"message": "ok"}, status.HTTP_201_CREATED)
    return Response(objeto_serialized.errors, status=status.HTTP_400_BAD_REQUEST)
            

@api_view(["POST", "GET","DELETE"])
@permission_classes([IsAuthenticated])     
def OrderViewById(request, orderid):
    if request.user.groups.filter(name="Manager").exists():
        if request.method == "DELETE":
                try:
                    objeto = OrderItem.objects.get(id=orderid)
                except OrderItem.DoesNotExist:
                    return Response({"message": "order does not exist"}, status=status.HTTP_404_NOT_FOUND)
                objeto.delete()
                return Response({"message": "order deleted."}, status=status.HTTP_200_OK)
            
       
        
    
    
    if request.method == "GET":
            try:
                items = OrderItem.objects.get(id=orderid)
            except OrderItem.DoesNotExist:
                return Response({"message": "order does not exist"}, status=status.HTTP_404_NOT_FOUND)
            serialized_item = OrderItemSerializer(items)
            return Response(serialized_item.data, status=status.HTTP_200_OK)
# Create your views here.

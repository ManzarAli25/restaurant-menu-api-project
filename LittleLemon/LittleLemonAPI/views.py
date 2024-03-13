from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import MenuItem,Category
from .serializers import MenuItemSerializer

# Create your views here.
# class MenuItemView(generics.ListCreateAPIView):
#     queryset = MenuItem.objects.all()
#     serializer_class = MenuItemSerializer
    
    
class SingleMenuItemView(generics.RetrieveUpdateAPIView,generics.DestroyAPIView):
        queryset = MenuItem.objects.all()
        serializer_class = MenuItemSerializer
    
    
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import MenuItem
from .serializers import MenuItemSerializer

@api_view(['GET', 'POST'])
def menu_items(request):
    if request.method == 'GET':
        items = MenuItem.objects.select_related('category').all()

        # Getting query parameters from the URL
        category_slug = request.query_params.get('category')
        search = request.query_params.get('search')
        ordering = request.query_params.get("ordering")

        # Checking if the category parameter is present
        if category_slug:
            # Filtering the data based on the query
            items = items.filter(category__slug=category_slug)

        if search:
            # If you want to fetch data based on if it contains the search param or not
            # items = items.filter(title__contains=search)
            items = items.filter(title__startswith=search)
            # 'istartswith' and 'icontains' will make it case insensitive

        if ordering:
            # Ordering by with multiple fields
            ordering_fields = ordering.split(",")
            items = items.order_by(*ordering_fields)

        serialized_items = MenuItemSerializer(items, many=True)
        return Response(serialized_items.data)

    elif request.method == 'POST':
        serializer = MenuItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


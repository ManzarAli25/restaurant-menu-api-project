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
    
    
@api_view(['GET'])
def menu_items(request):
    items = MenuItem.objects.select_related('category').all()
    
    #getting query param from url
    category_slug = request.query_params.get('category')
    search = request.query_params.get('search')
    ordering = request.query_params.get("ordering")
    

    
    
    #checking if the param is present
    if category_slug:
        #filtering the data based on the query
        items = items.filter(category__slug=category_slug)
        
        
    if search:
        #if you want t0o fetch data based on if it contains the search param or not
        # items= items.filter(title__contains=search)
        
        items= items.filter(title__startswith=search)
        # 'istartswith' and 'icontains' will make it case insensitive
        
    # if ordering:
    #     items = items.order_by(ordering) 
    #     # sorting with price 
    
    if ordering:
        ordering_fields = ordering.split(",")
        items= items.order_by(*ordering_fields)
    
    serialized_items = MenuItemSerializer(items, many=True)
    return Response(serialized_items.data)

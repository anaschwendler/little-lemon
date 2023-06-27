from rest_framework import generics
from .models import MenuItem, Category
from .serializers import MenuItemSerializer, CategorySerializer
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage

from rest_framework.renderers import StaticHTMLRenderer
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes, permission_classes, throttle_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle


# Create your views here.
class MenuItemsView(generics.ListCreateAPIView):
    throttle_classes = [AnonRateThrottle]
    serializer_class = MenuItemSerializer
    
    def get_queryset(self):
        queryset = MenuItem.objects.select_related('category').all()
        category_name = self.request.query_params.get('category')
        to_price = self.request.query_params.get('to_price')
        search = self.request.query_params.get('search')
        ordering = self.request.query_params.get('ordering')
        perpage = self.request.query_params.get('perpage', default=2)
        page = self.request.query_params.get('page',default=1)
        if category_name:
            queryset = queryset.filter(category__title=category_name)
        if to_price:
            queryset = queryset.filter(price__lte=to_price)
        if search:
            # icontains = case insenstive
            queryset = queryset.filter(title__icontains=search)
        if ordering:
            ordering_fields = ordering.split(",")
            queryset = queryset.order_by(*ordering_fields)
        paginator = Paginator(queryset, per_page=perpage)
        try:
            queryset = paginator.page(number=page)
        except EmptyPage:
            queryset = []
        return queryset

class SingleMenuItemView(generics.RetrieveUpdateAPIView, generics.DestroyAPIView):
    queryset = MenuItem.objects.select_related('category').all()
    serializer_class = MenuItemSerializer
    
class CategoryView(generics.ListCreateAPIView):
    queryset = Category.objects.select_related('category').all()
    serializer_class = CategorySerializer
    
class SingleCategoryView(generics.RetrieveUpdateAPIView, generics.DestroyAPIView):
    queryset = Category.objects.select_related('category').all()
    serializer_class = CategorySerializer
    
@api_view(["GET"])
@renderer_classes([StaticHTMLRenderer])
def welcome(request):
    data = '<html><body><h1>Welcome To Little Lemon API Project</h1></body></html>'
    return Response(data)

@api_view()
@permission_classes([IsAuthenticated])
def secret(request):
    return Response({'message':'Some secret message'})

@api_view()
@permission_classes([IsAuthenticated])
def manager_view(request):
    if request.user.groups.filter(name='Manager').exists():
        return Response({'message':'Only manager should see it'})
    else:
        return Response({'message':'You are not authorized'})
    
@api_view()
@throttle_classes([AnonRateThrottle])
def throttle_check(request):
    return Response({'message':'successful'})
    
@api_view()
@permission_classes([IsAuthenticated])
@throttle_classes([UserRateThrottle])
def throttle_check_auth(request):
    return Response({'message':'successful, only for auth users'})
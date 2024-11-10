from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework import status, filters, permissions, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model, authenticate, login, update_session_auth_hash, logout
from rest_framework.pagination import PageNumberPagination

from orders.models import Order
from products.models import Product, Basket
from products.serializers import ProductSerializer, BasketSerializer
from orders.serializers import OrderSerializer
from users.models import EmailVerification
from users.serializers import UserSerializer, UserRegistrationSerializer, UserProfileSerializer
from .authentication import CustomTokenAuthentication

User = get_user_model()


class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.initiator == request.user or request.user.is_staff


# ProductModelViewSet
class ProductModelViewSet(ModelViewSet):
    queryset = Product.objects.all().select_related('category').prefetch_related('tags')
    serializer_class = ProductSerializer
    filterset_fields = ['category', 'price']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'price', 'id']
    pagination_class = PageNumberPagination

    def get_permissions(self):
        if self.action in ('create', 'update', 'destroy'):
            self.permission_classes = (IsAdminUser,)
        return super(ProductModelViewSet, self).get_permissions()


# BasketModelViewSet
class BasketModelViewSet(ModelViewSet):
    queryset = Basket.objects.all()
    serializer_class = BasketSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    pagination_class = None

    def get_queryset(self):
        queryset = super(BasketModelViewSet, self).get_queryset()
        return queryset.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        try:
            product_id = request.data['product_id']
            products = Product.objects.filter(id=product_id)
            if not products.exists():
                return Response({'product_id': 'There is no product with this ID.'}, status=status.HTTP_400_BAD_REQUEST)
            obj, is_created = Basket.create_or_update(products.first().id, self.request.user)
            status_code = status.HTTP_201_CREATED if is_created else status.HTTP_200_OK
            serializer = self.get_serializer(obj)
            return Response(serializer.data, status=status_code)
        except KeyError:
            return Response({'product_id': 'The field is required.'}, status=status.HTTP_400_BAD_REQUEST)


# OrderModelViewSet


class OrderModelViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]  # Require authentication
    pagination_class = PageNumberPagination

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(initiator=user)

    def perform_create(self, serializer):
        serializer.save(initiator=self.request.user)

    def perform_update(self, serializer):
        if self.request.user != serializer.instance.initiator and not self.request.user.is_staff:
            raise PermissionDenied("You do not have permission to edit this order.")
        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user != instance.initiator and not self.request.user.is_staff:
            raise PermissionDenied("You do not have permission to delete this order.")
        instance.delete()


# User Login API
class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return Response(UserSerializer(user).data)
        return Response({'error': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)


# Registration API View
class UserRegistrationAPIView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        user = serializer.save(is_no_social_user=True)
        return user


# Logout API View
class UserLogoutAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)

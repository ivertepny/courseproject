from django.urls import path, include
from rest_framework import routers
from api.viewsets import ProductModelViewSet, OrderModelViewSet, BasketModelViewSet, \
    UserLoginAPIView, UserLogoutAPIView, UserRegistrationAPIView  # , register_user, logout_user
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.authtoken.views import obtain_auth_token

app_name = 'api'  # Не зрозумів для чого

router = routers.DefaultRouter()
router.register(r'products', ProductModelViewSet)
router.register(r'orders', OrderModelViewSet)
router.register(r'baskets', BasketModelViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title="Store API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="ivertepny@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('', include(router.urls)),
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('auth-token/', obtain_auth_token),
    path('user/login/', UserLoginAPIView.as_view(), name='api_login'),
    path('user/logout/', UserLogoutAPIView.as_view(), name='api_logout'),
    path('user/registration/', UserRegistrationAPIView.as_view(), name='api_register'),

]

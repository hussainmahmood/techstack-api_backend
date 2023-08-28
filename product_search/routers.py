from rest_framework import routers
from .views import AuthViewSet, UserViewSet, ProductViewSet

router = routers.DefaultRouter()
router.register(r"auth", AuthViewSet, basename="auth")
router.register(r"user", UserViewSet, basename="user")
router.register(r"product", ProductViewSet, basename="product")
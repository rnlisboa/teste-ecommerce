from django.urls import path
from rest_framework import routers
from .views import *


router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register(r'products', ProductViewSet)
urlpatterns = router.urls
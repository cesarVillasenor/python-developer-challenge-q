from django.urls import path, include
from .api.viewsets import *
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

router = routers.DefaultRouter()
router.register(r'', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
] + format_suffix_patterns([
    path(r'<int:user_id>/addresses', CreateAddressView.as_view(), name="create-address"),
    path(r'<int:user_id>/update-password', PasswordResetView.as_view(), name="password-reset"),
    path(r'<int:user_id>/addresses/<int:address_id>', UpdatePrimaryAddressView.as_view(), name="update-address"),
])

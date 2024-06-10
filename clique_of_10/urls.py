from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter
from users.views import UserViewSet, GroupViewSet, get_csrf_token

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/csrf-token/', get_csrf_token, name='get_csrf_token'),
    path('api/', include(router.urls)),
]

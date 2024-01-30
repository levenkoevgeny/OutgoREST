from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView
from django.conf.urls.static import static
from django.conf import settings

from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from outgo import views as outgo_views

router = routers.DefaultRouter()
router.register(r'users', outgo_views.CustomUserViewSet)
router.register(r'subdivisions', outgo_views.SubdivisionViewSet, basename='subdivisions')
router.register(r'employee-kinds', outgo_views.EmployeeKindViewSet)
router.register(r'sheet-items', outgo_views.SheetItemViewSet)
router.register(r'outgo-kinds', outgo_views.OutgoKindViewSet)
router.register(r'outgo', outgo_views.OutgoViewSet)
router.register(r'outgo-data', outgo_views.OutgoDataViewSet, basename='outgo-data')

urlpatterns = [
    path('', RedirectView.as_view(url='/api')),
    path('api/users/me/', outgo_views.get_me),
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
]

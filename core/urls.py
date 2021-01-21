from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = format_suffix_patterns([
    path("city/", views.CityViewSet.as_view({'get': 'list'})),
    path("city/<int:pk>/", views.CityViewSet.as_view({'get': 'retrieve'})),
    path("step/", views.StepViewSet.as_view({'get': 'list'})),
    path("step/<int:pk>/", views.StepViewSet.as_view({'post': 'create', 'get': 'retrieve'})),
])

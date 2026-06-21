from django.urls import path
from .views import home,property_detail
from .views import *

urlpatterns = [
    path('', home),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path(
        'property/<int:id>/',
        property_detail
    ),
    path(
    'favorite/<int:id>/',
    add_favorite,
    name='favorite'
    ),
    path('api/properties/', api_properties),
    path('api/property/<int:id>/', api_property),
]
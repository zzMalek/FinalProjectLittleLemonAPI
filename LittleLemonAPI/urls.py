from django.urls import path

from . import views




urlpatterns = [
    path("menu-items/", views.MenuItemView),
    path('menu-items/<int:pk>/', views.SingleMenuItemView, name='single-menu-item'),
    path("groups/manager/users/", views.managers),
    path("groups/manager/users/<int:pk>", views.managers_remove),
    path("groups/delivery-crew/users/", views.delivery),
    path("groups/delivery-crew/users/<int:pk>", views.delivery_remove),
    path("cart/menu-items", views.customer),
    path("orders/", views.OrderView),
    path("orders/<int:orderid>/", views.OrderViewById),
    
]

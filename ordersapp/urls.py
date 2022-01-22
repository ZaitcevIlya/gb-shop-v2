
from django.urls import path
from ordersapp.views import OrderListView, CreateOrderView, UpdateOrderView, DeleteOrderView, DetailOrderView, order_forming_complete

app_name = 'ordersapp'
urlpatterns = [
    path('',  OrderListView.as_view(), name='list'),
    path('create/', CreateOrderView.as_view(), name='create'),
    path('update/<int:pk>/', UpdateOrderView.as_view(), name='update'),
    path('read/<int:pk>/', DetailOrderView.as_view(), name='read'),
    path('delete/<int:pk>/', DeleteOrderView.as_view(), name='delete'),
    path('forming_complete/<int:pk>/', order_forming_complete, name='forming_complete'),
]

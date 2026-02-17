from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    # Purchase Orders
    path("purchase-orders/", views.po_list, name="po_list"),
    path("purchase-orders/add/", views.po_create, name="po_create"),
    path("purchase-orders/<int:pk>/", views.po_detail, name="po_detail"),
    path("purchase-orders/<int:pk>/edit/", views.po_update, name="po_update"),
    path("purchase-orders/<int:pk>/delete/", views.po_delete, name="po_delete"),
    # Sales Orders
    path("sales-orders/", views.so_list, name="so_list"),
    path("sales-orders/add/", views.so_create, name="so_create"),
    path("sales-orders/<int:pk>/", views.so_detail, name="so_detail"),
    path("sales-orders/<int:pk>/edit/", views.so_update, name="so_update"),
    path("sales-orders/<int:pk>/delete/", views.so_delete, name="so_delete"),
]

from django.urls import path
from . import views


app_name = "management"

urlpatterns = [
    path('products/', views.product_list_view, name='product_list'),
    path('dashboard/', views.dashboard_view, name='dashboard_view'),
    path("products/create/", views.product_create_view, name="product_create"),
    path("products/<product_id>/delete/", views.product_delete_view, name="product_delete_view"),
]
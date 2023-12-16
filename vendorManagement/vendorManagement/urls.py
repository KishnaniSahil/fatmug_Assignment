"""
URL configuration for vendorManagement project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from purchase_orders.views import PurchaseOrderCreateView, PurchaseOrderDeleteView, PurchaseOrderDetailView, PurchaseOrderListView, PurchaseOrderUpdateView

from vendorManagementSystem.views import VendorCreateView, VendorDeleteView, VendorDetailView, VendorListView, VendorPerformanceView, VendorUpdateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/vendors/', VendorCreateView.as_view(), name='vendor-create'),
    path('api/vendors/list/', VendorListView.as_view(), name='vendor-list'),
    path('api/vendors/<int:vendor_id>/', VendorDetailView.as_view(), name='vendor-detail'),
    path('api/vendors/<int:vendor_id>/update/', VendorUpdateView.as_view(), name='vendor-update'),
    path('api/vendors/<int:vendor_id>/delete/', VendorDeleteView.as_view(), name='vendor-delete'),
    path('api/vendors/<int:vendor_id>/performance/', VendorPerformanceView.as_view(), name='vendor-performance'), 
    path('api/purchase_orders/', PurchaseOrderCreateView.as_view(), name='purchase-order-create'),
   # path('api/purchase_orders/', PurchaseOrderListView.as_view(), name='purchase-order-list'),
    path('api/purchase_orders/list/', PurchaseOrderListView.as_view(), name='purchase-order-list'),  # Changed path
    path('api/purchase_orders/<int:po_id>/', PurchaseOrderDetailView.as_view(), name='purchase-order-detail'),
   path('api/purchase_orders/update/<int:po_id>/', PurchaseOrderUpdateView.as_view(), name='purchase-order-update'), 
   path('api/purchase_orders/delete/<int:po_id>/', PurchaseOrderDeleteView.as_view(), name='purchase-order-delete'),

]

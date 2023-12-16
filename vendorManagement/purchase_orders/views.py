import json
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from purchase_orders.models import PurchaseOrder
from vendorManagementSystem.models import Vendor

# Create your views here.
@method_decorator(csrf_exempt, name='dispatch')
class PurchaseOrderCreateView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            po_number = data.get("po_number")
            vendor_id = data.get("vendor_id")
            order_date = data.get("order_date")
            delivery_date = data.get("delivery_date")
            items = data.get("items")
            quantity = data.get("quantity")
            status = data.get("status", "pending")  # Default to 'pending'
            quality_rating = data.get("quality_rating")
            issue_date = data.get("issue_date")
            acknowledgment_date = data.get("acknowledgment_date")

            # Ensure the vendor exists
            vendor = get_object_or_404(Vendor, pk=vendor_id)

            # Create a new purchase order and save it to the database
            purchase_order = PurchaseOrder(
                po_number=po_number,
                vendor=vendor,
                order_date=order_date,
                delivery_date=delivery_date,
                items=items,
                quantity=quantity,
                status=status,
                quality_rating=quality_rating,
                issue_date=issue_date,
                acknowledgment_date=acknowledgment_date
            )
            purchase_order.save()

            # Return the purchase order details in the response
            response_data = {
                "id": purchase_order.id,
                "po_number": purchase_order.po_number,
                "vendor_id": purchase_order.vendor_id,
                "order_date": purchase_order.order_date,
                "delivery_date": purchase_order.delivery_date,
                "items": purchase_order.items,
                "quantity": purchase_order.quantity,
                "status": purchase_order.status,
                "quality_rating": purchase_order.quality_rating,
                "issue_date": purchase_order.issue_date,
                "acknowledgment_date": purchase_order.acknowledgment_date,
            }

            return JsonResponse(response_data, status=201)  # 201 Created

        except Exception as e:
            return JsonResponse({"error": f"Error creating purchase order: {str(e)}"}, status=400)
        
@method_decorator(csrf_exempt, name='dispatch')
class PurchaseOrderListView(View):
    def get(self, request, *args, **kwargs):
        try:
            vendor_id = request.GET.get('vendor_id')

            # If vendor_id is provided, filter purchase orders by vendor
            if vendor_id:
                purchase_orders = PurchaseOrder.objects.filter(vendor__id=vendor_id)
            else:
                purchase_orders = PurchaseOrder.objects.all()

            # Serialize the purchase orders
            purchase_orders_data = [
                {
                    "id": order.id,
                    "po_number": order.po_number,
                    "vendor_id": order.vendor.id,
                    "order_date": order.order_date,
                    "delivery_date": order.delivery_date,
                    "items": order.items,
                    "quantity": order.quantity,
                    "status": order.status,
                    "quality_rating": order.quality_rating,
                    "issue_date": order.issue_date,
                    "acknowledgment_date": order.acknowledgment_date,
                }
                for order in purchase_orders
            ]

            return JsonResponse(purchase_orders_data, safe=False)

        except Exception as e:
            return JsonResponse({"error": f"Error retrieving purchase orders: {str(e)}"}, status=400)
        
@method_decorator(csrf_exempt, name='dispatch')
class PurchaseOrderDetailView(View):
    def get(self, request, po_id, *args, **kwargs):
        try:
            purchase_order = PurchaseOrder.objects.get(id=po_id)

            # Serialize the purchase order details
            purchase_order_data = {
                "id": purchase_order.id,
                "po_number": purchase_order.po_number,
                "vendor_id": purchase_order.vendor.id,
                "order_date": purchase_order.order_date,
                "delivery_date": purchase_order.delivery_date,
                "items": purchase_order.items,
                "quantity": purchase_order.quantity,
                "status": purchase_order.status,
                "quality_rating": purchase_order.quality_rating,
                "issue_date": purchase_order.issue_date,
                "acknowledgment_date": purchase_order.acknowledgment_date,
            }

            return JsonResponse(purchase_order_data, safe=False)

        except PurchaseOrder.DoesNotExist:
            return JsonResponse({"error": f"Purchase Order with id {po_id} does not exist."}, status=404)

        except Exception as e:
            return JsonResponse({"error": f"Error retrieving purchase order details: {str(e)}"}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class PurchaseOrderUpdateView(View):
    def put(self, request, po_id, *args, **kwargs):
        try:
            # Retrieve the purchase order
            purchase_order = PurchaseOrder.objects.get(id=po_id)

            # Parse the request body as JSON
            data = json.loads(request.body)

            # Update the purchase order fields
            purchase_order.delivery_date = data.get('delivery_date', purchase_order.delivery_date)
            purchase_order.items = data.get('items', purchase_order.items)
            purchase_order.quantity = data.get('quantity', purchase_order.quantity)
            purchase_order.status = data.get('status', purchase_order.status)
            purchase_order.quality_rating = data.get('quality_rating', purchase_order.quality_rating)
            purchase_order.acknowledgment_date = data.get('acknowledgment_date', purchase_order.acknowledgment_date)

            # Save the updated purchase order
            purchase_order.save()

            # Serialize the updated purchase order details
            purchase_order_data = {
                "id": purchase_order.id,
                "po_number": purchase_order.po_number,
                "vendor_id": purchase_order.vendor.id,
                "order_date": purchase_order.order_date,
                "delivery_date": purchase_order.delivery_date,
                "items": purchase_order.items,
                "quantity": purchase_order.quantity,
                "status": purchase_order.status,
                "quality_rating": purchase_order.quality_rating,
                "issue_date": purchase_order.issue_date,
                "acknowledgment_date": purchase_order.acknowledgment_date,
            }

            return JsonResponse(purchase_order_data, safe=False)

        except PurchaseOrder.DoesNotExist:
            return JsonResponse({"error": f"Purchase Order with id {po_id} does not exist."}, status=404)

        except Exception as e:
            return JsonResponse({"error": f"Error updating purchase order: {str(e)}"}, status=400)     

@method_decorator(csrf_exempt, name='dispatch')
class PurchaseOrderDeleteView(View):
    def delete(self, request, po_id, *args, **kwargs):
        try:
            # Retrieve the purchase order
            purchase_order = PurchaseOrder.objects.get(id=po_id)

            # Delete the purchase order
            purchase_order.delete()

            return JsonResponse({"message": f"Purchase Order with id {po_id} has been deleted successfully."})

        except PurchaseOrder.DoesNotExist:
            return JsonResponse({"error": f"Purchase Order with id {po_id} does not exist."}, status=404)

        except Exception as e:
            return JsonResponse({"error": f"Error deleting purchase order: {str(e)}"}, status=400)                   
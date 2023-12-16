import json
from django.db import IntegrityError
from django.forms import DurationField
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.models import Avg, ExpressionWrapper, F, DurationField

from purchase_orders.models import PurchaseOrder
from .models import Vendor

# Create your views here.
@method_decorator(csrf_exempt, name='dispatch')
class VendorCreateView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            name = data.get("name")
            contact_details = data.get("contact_details")
            address = data.get("address")
            vendor_code = data.get("vendor_code")

            # Check if the vendor with the given vendor code already exists
            if Vendor.objects.filter(vendor_code=vendor_code).exists():
                return JsonResponse({"error": "Vendor with the given vendor code already exists."}, status=400)

            # Create a new vendor and save it to the database
            vendor = Vendor(name=name, contact_details=contact_details, address=address, vendor_code=vendor_code)
            vendor.save()

            # Return the vendor's ID in the response
            return JsonResponse({"id": vendor.id})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
        
@method_decorator(csrf_exempt, name='dispatch')
class VendorListView(View):
    def get(self, request, *args, **kwargs):
        vendors = Vendor.objects.all()
        vendor_list = [{"id": vendor.id, "name": vendor.name, "vendor_code": vendor.vendor_code} for vendor in vendors]
        return JsonResponse(vendor_list, safe=False)

@method_decorator(csrf_exempt, name='dispatch')
class VendorDetailView(View):
    def get(self, request, vendor_id, *args, **kwargs):
        vendor = get_object_or_404(Vendor, pk=vendor_id)
        vendor_details = {
            "id": vendor.id,
            "name": vendor.name,
            "contact_details": vendor.contact_details,
            "address": vendor.address,
            "vendor_code": vendor.vendor_code,
            "on_time_delivery_rate": vendor.on_time_delivery_rate,
            "quality_rating_avg": vendor.quality_rating_avg,
            "average_response_time": vendor.average_response_time,
            "fulfillment_rate": vendor.fulfillment_rate,
        }
        return JsonResponse(vendor_details)

@method_decorator(csrf_exempt, name='dispatch')
class VendorUpdateView(View):
    def put(self, request, vendor_id, *args, **kwargs):
        try:
            vendor = get_object_or_404(Vendor, pk=vendor_id)
            data = json.loads(request.body)

            # Update vendor fields
            vendor.name = data.get("name", vendor.name)
            vendor.contact_details = data.get("contact_details", vendor.contact_details)
            vendor.address = data.get("address", vendor.address)
            vendor.vendor_code = data.get("vendor_code", vendor.vendor_code)

            # Save the updated vendor details to the database
            vendor.save()

            # Return the updated vendor details
            updated_vendor_details = {
                "id": vendor.id,
                "name": vendor.name,
                "contact_details": vendor.contact_details,
                "address": vendor.address,
                "vendor_code": vendor.vendor_code,
                "on_time_delivery_rate": vendor.on_time_delivery_rate,
                "quality_rating_avg": vendor.quality_rating_avg,
                "average_response_time": vendor.average_response_time,
                "fulfillment_rate": vendor.fulfillment_rate,
            }

            return JsonResponse(updated_vendor_details)

        except IntegrityError as e:
            return JsonResponse({"error": "Vendor code must be unique."}, status=400)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class VendorDeleteView(View):
    def delete(self, request, vendor_id, *args, **kwargs):
        try:
            vendor = get_object_or_404(Vendor, pk=vendor_id)
            vendor.delete()
            
            return JsonResponse({"message": f"Vendor with ID {vendor_id} has been deleted."})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class VendorPerformanceView(View):
    def get(self, request, vendor_id, *args, **kwargs):
        vendor = get_object_or_404(Vendor, pk=vendor_id)

        # Calculate On-Time Delivery Rate
        completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
        on_time_deliveries = completed_pos.filter(delivery_date__lte=F('acknowledgment_date'))
        on_time_delivery_rate = (on_time_deliveries.count() / completed_pos.count()) * 100 if completed_pos.count() > 0 else 0

        # Calculate Quality Rating Average
        completed_pos_with_rating = completed_pos.exclude(quality_rating__isnull=True)
        quality_rating_avg = completed_pos_with_rating.aggregate(avg_rating=Avg('quality_rating'))['avg_rating'] or 0

        # Calculate Average Response Time
        response_times = completed_pos.exclude(acknowledgment_date__isnull=True).annotate(
            response_time=ExpressionWrapper(
                F('acknowledgment_date') - F('issue_date'),
                output_field=DurationField()
            )
        )
        average_response_time = response_times.aggregate(avg_response_time=Avg('response_time'))['avg_response_time'] or 0

        # Convert average_response_time to hours
        average_response_time_hours = average_response_time.total_seconds() / 3600 if average_response_time else 0

        # Calculate Fulfilment Rate
        successfully_fulfilled_pos = completed_pos.filter(issue_date__lte=F('acknowledgment_date'))
        fulfillment_rate = (successfully_fulfilled_pos.count() / completed_pos.count()) * 100 if completed_pos.count() > 0 else 0

        # Return the calculated performance metrics
        performance_metrics = {
            "on_time_delivery_rate": on_time_delivery_rate,
            "quality_rating_avg": quality_rating_avg,
            "average_response_time": average_response_time_hours,
            "fulfillment_rate": fulfillment_rate,
        }

        return JsonResponse(performance_metrics)
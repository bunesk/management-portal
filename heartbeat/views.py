from django.shortcuts import render
from django.shortcuts import render, redirect
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .controllers import HeartbeatController
from datetime import datetime
from rest_framework.decorators import api_view
from .models import Heartbeat
from licenses.models import LocationLicense, CustomerLicense, UsedSoftwareProduct
from customers.models import Location
import json


def index(request: WSGIRequest) -> HttpResponseRedirect:
    """
    When the app root is called. Redirects to the heartbeat list.

    Parameters:
    request (WSGIRequest): url request of the user

    Returns:
    HttpResponseRedirect: redirection to the heartbeat list
    """
    return redirect('heartbeat_list')

def heartbeat_list(request: WSGIRequest) -> HttpResponse:
    """
    When the heartbeat list is called. Renders the heartbeat list.

    Parameters:
    request (WSGIRequest): url request of the user

    Returns:
    HttpResponse: heartbeat list
    """
    used_products = HeartbeatController.read()
    count_missing = HeartbeatController.get_count_missing(used_products)
    context       = {
        'used_products' : used_products,
        'count_missing' : count_missing,
    }
    return render(request, 'heartbeat/list.html', context)

def history(request: WSGIRequest) -> JsonResponse:
    """
    When the history is called as an ajax request.
    Gives the data of the heartbeats of a given used product id.

    Parameters:
    request (WSGIRequest): ajax request

    Returns:
    JsonResponse: heartbeats
    """
    response = JsonResponse({})
    if request.is_ajax():
        id = request.POST.get('id', '')
        if len(id):
            heartbeats = HeartbeatController.get_heartbeats_for_used_product_id(id = int(id))
            context = {
                'heartbeats': json.dumps(heartbeats),
            }
            response = JsonResponse(context)
    
    return response

# API für den Empfang des Heartbeats
@api_view(["POST"])
def heartbeat(request):

    print(request.data)

    beat = {
        "key": request.POST.get('key'),
        "log": request.POST.get('log')
    }

    beat["key"] = beat["key"].replace("\n", "")

    # Filtern des genutztes_produkt_ID
    try:
        location_license = LocationLicense.objects.get(key=beat["key"])
        print(location_license.key)
        used_software_product = UsedSoftwareProduct.objects.get(
            location = location_license.location,
            product  = location_license.module.product,
        )
        Heartbeat.objects.create(used_product=used_software_product, message=beat["key"], detail=beat["log"])
    except:
        try:
            customer_license = CustomerLicense.objects.get(key=beat["key"])
            print(customer_license.key)
            locations = Location.objects.filter(customer = customer_license.customer)
            for location in locations:
                used_software_product = UsedSoftwareProduct.objects.get(
                    location = location,
                    product  = customer_license.module.product,
                )
                break
            Heartbeat.objects.create(used_product=used_software_product, message=beat["key"], detail=beat["log"], unknown_location = True)
        except:
            pass

    return JsonResponse({})

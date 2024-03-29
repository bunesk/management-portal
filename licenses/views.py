from django.shortcuts import render, redirect
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from datetime import datetime, timezone
from rest_framework.decorators import api_view

from customers.models import Location
from heartbeat.controllers import HeartbeatController
from heartbeat.models import Heartbeat
from .controllers import LicenseController, SoftwareModuleController
from customers.controllers import CustomerController, LocationController
from .models import LocationLicense, UsedSoftwareProduct, CustomerLicense, License
import json


def index(request: WSGIRequest) -> HttpResponseRedirect:
    """
    When the app root is called. Redirects to the license list.

    Parameters:
    request (WSGIRequest): url request of the user

    Returns:
    HttpResponseRedirect: redirection to the license list
    """
    return redirect('licenses_list')

def licenses_list(request: WSGIRequest) -> HttpResponse:
    """
    When the license list is called. Renders the license list.

    Parameters:
    request (WSGIRequest): url request of the user

    Returns:
    HttpResponse: license list
    """
    status     = request.COOKIES.get('license_status_status')
    message    = request.COOKIES.get('license_status_message')
    heartbeats = HeartbeatController.read()
    licenses   = LicenseController.read()
    context    = {
        'heartbeats': heartbeats,
        'licenses'  : licenses,
        'status'    : status,
        'message'   : message,
    }

    response = render(request, 'licenses/list.html', context)
    response.delete_cookie('license_status_status')
    response.delete_cookie('license_status_message')

    return response

def create(request: WSGIRequest) -> HttpResponse:
    """
    When the license create is called. Renders the form to create a license.

    Parameters:
    request (WSGIRequest): url request of the user

    Returns:
    HttpResponse: form to create license
    """
    heartbeats = HeartbeatController.read()
    modules    = SoftwareModuleController.get_module_names()
    locations  = LocationController.get_location_names()
    customers  = CustomerController.get_customer_names()
    context    = {
        'title'     : 'Lizenz erstellen',
        'heartbeats': heartbeats,
        'modules'   : modules,
        'locations' : locations,
        'customers' : customers,
    }
    return render(request, 'licenses/edit.html', context)

def edit(request: WSGIRequest, id: int = 0) -> HttpResponse:
    """
    When the license edit is called.
    Renders the form to edit the license with the given id. 

    Parameters:
    request (WSGIRequest): url request of the user
    id      (int)        : id of the license to edit

    Returns:
    HttpResponse: form to edit license
    """
    if id < 1:
        return redirect('licenses_list')

    license    = LicenseController.get_license_by_id(id = id)
    heartbeats = HeartbeatController.read()
    modules    = SoftwareModuleController.get_module_names()
    locations  = LocationController.get_location_names()
    customers  = CustomerController.get_customer_names()
    context    = {
        'title'     : 'Lizenz bearbeiten',
        'license'   : license,
        'heartbeats': heartbeats,
        'modules'   : modules,
        'locations' : locations,
        'customers' : customers,
    }
    return render(request, 'licenses/edit.html', context)

def create_replace_license(request: WSGIRequest, old_license_id: int = 0) -> HttpResponse:
    """
    When the replace license create is called.
    Renders the form to create the replacing license with the given id of the license to replace. 

    Parameters:
    request        (WSGIRequest): url request of the user
    old_license_id (int)        : id of the license to replace

    Returns:
    HttpResponse: form to create replacing license
    """
    if old_license_id < 1:
        return redirect('licenses_list')

    old_license = LicenseController.get_license_by_id(id = old_license_id)
    heartbeats  = HeartbeatController.read()
    context     = {
        'title'      : 'Zukunftslizenz erstellen',
        'old_license': old_license,
        'heartbeats' : heartbeats,
    }
    return render(request, 'licenses/edit-replace.html', context)

def edit_replace_license(request: WSGIRequest, old_license_id: int = 0, id: int = 0) -> HttpResponse:
    """
    When the replace license edit is called.
    Renders the form to edit the replacing license with the given id of the license to replace and the license to edit. 

    Parameters:
    request        (WSGIRequest): url request of the user
    id             (int)        : id of the license to edit
    old_license_id (int)        : id of the license to replace

    Returns:
    HttpResponse: form to edit replacing license
    """
    if id < 1 or old_license_id < 1:
        return redirect('licenses_list')

    license     = LicenseController.get_license_by_id(id = id)
    old_license = LicenseController.get_license_by_id(id = old_license_id)
    heartbeats  = HeartbeatController.read()
    context     = {
        'title'      : 'Zukunftslizenz bearbeiten',
        'license'    : license,
        'old_license': old_license,
        'heartbeats' : heartbeats,
    }
    return render(request, 'licenses/edit-replace.html', context)

def save(request: WSGIRequest) -> JsonResponse:
    """
    When the license save is called as an ajax request.
    Saves the data sent if valid and complete and returns the status.
    If an id is also sent this license will be edited, otherwise a new one will be created.

    Parameters:
    request (WSGIRequest): ajax save request

    Returns:
    JsonResponse: save status
    """
    response = JsonResponse({})
    if request.is_ajax():
        id              = request.POST.get('id', '')
        key             = request.POST.get('key', '')
        detail          = request.POST.get('detail', '')
        start_date      = request.POST.get('start_date', '')
        end_date        = request.POST.get('end_date', '')
        module          = request.POST.get('module', '')
        location        = request.POST.get('location', '')
        customer        = request.POST.get('customer', '')
        replace_license = request.POST.get('replace_license', '')

        status      = LicenseController.save(
            id              = id,
            key             = key,
            detail          = detail,
            start_date      = start_date,
            end_date        = end_date,
            module          = module,
            location        = location,
            customer        = customer,
            replace_license = replace_license,
        )
        response = JsonResponse(status.__dict__)
        if status.status:
            response.set_cookie('license_status_status' , status.status , 7)
            response.set_cookie('license_status_message', status.message, 7)

    return response

def delete(request: WSGIRequest, id: int = 0) -> HttpResponseRedirect:
    """
    When the license delete is called. Deletes the license with the given id.
    After that it redirects to the license list.

    Parameters:
    request (WSGIRequest): url request of the user

    Returns:
    HttpResponseRedirect: redirection to the license list
    """
    response = redirect('licenses_list')
    if id > 0:
        status = LicenseController.delete(id = id)
        response.set_cookie('license_status_status' , status.status , 7)
        response.set_cookie('license_status_message', status.message, 7)

    return response

def settings(request: WSGIRequest) -> JsonResponse:
    """
    When the license settings is called as an ajax request.
    Gets information about current and future license by current license id.

    Parameters:
    request (WSGIRequest): ajax request

    Returns:
    JsonResponse: license information
    """
    response = JsonResponse({})
    if request.is_ajax():
        id = request.POST.get('id', '')

        licenses = LicenseController.get_settings_information(id = id)
        response = JsonResponse(licenses)

    return response

@api_view(["POST"])
def license_heartbeat(request: WSGIRequest) -> JsonResponse:
    """
    This function should be triggered by a request from the customer's license script.
    It checks if the license is (still) valid by given key.
    If a newer license is there it sends the key of it in the response.

    Parameters:
    request (WSGIRequest): post request from the license script

    Returns:
    JsonResponse: new license key if needed
    """
    key     = request.POST.get("key").replace('\n', '')
    license = None

    try:
        license = License.objects.get(key = key)
    except:
        return JsonResponse({})
    
    current_date = datetime.now(timezone.utc)
    context      = {
        "key"    : '',
        "exist"  : False,
    }

    if license and (license.end_date < current_date):
        try:
            future_license    = License.objects.get(replace_license__key = license.key)
            context['key']    = future_license.key
            context['exist']  = True
        except:
            pass

    return JsonResponse(context)

@api_view(["POST"])
def license_heartbeat_save(request: WSGIRequest) -> JsonResponse:
    """
    This function should be triggered by a request from the customer's license script.
    It replaces the new given license with the old one and deletes the future license.
    If the license is a customer license the replacement only happens if all locations
    already have the new license.

    Parameters:
    request (WSGIRequest): post request from the license script

    Returns:
    JsonResponse: new license key if needed
    """
    new_exists = request.POST.get('new_exists', '')

    if new_exists == "True":
        new_key = request.POST.get('new', '').replace('\n', '')
        old_key = request.POST.get('old', '').replace('\n', '')

        try:
            new_license                 = LocationLicense.objects.get(key = new_key)
            old_license                 = LocationLicense.objects.get(key = old_key)
            old_license.key             = new_license.key
            old_license.detail          = new_license.detail
            old_license.start_date      = new_license.start_date
            old_license.end_date        = new_license.end_date
            new_license.delete()
            old_license.save()
        except:
            try:
                new_license = CustomerLicense.objects.get(key = new_key)
                new_license.replace_count += 1
                total_count = len(Location.objects.filter(customer = new_license.customer))
                if new_license.replace_count >= total_count:
                    old_license                 = CustomerLicense.objects.get(key = old_key)
                    old_license.key             = new_license.key
                    old_license.detail          = new_license.detail
                    old_license.start_date      = new_license.start_date
                    old_license.end_date        = new_license.end_date
                    new_license.delete()
                    old_license.save()
                else:
                    new_license.save()
            except:
                pass

    return JsonResponse({})

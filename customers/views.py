from django.shortcuts import render, redirect
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, JsonResponse
from heartbeat.controllers import HeartbeatController
from customers.controllers import CustomerController
from .controllers import LocationController


def index(request: WSGIRequest) -> HttpResponse:
    return redirect('customers_list')

def customerList(request: WSGIRequest) -> HttpResponse:
    status       = request.COOKIES.get('customer_status_status')
    message      = request.COOKIES.get('customer_status_message')
    heartbeats   = HeartbeatController.read()
    customerList = CustomerController.getCustomersForEachLetter()
    customers    = CustomerController.read()
    context      = {
        'heartbeats'    : heartbeats,
        'customer_list' : customerList,
        'customers'     : customers,
        'status'        : status,
        'message'       : message,
    }

    response = render(request, 'customers/list.html', context = context)
    response.delete_cookie('customer_status_status')
    response.delete_cookie('customer_status_message')

    return response

def customer(request: WSGIRequest, id: int = 0):
    response = None
    if request.is_ajax and id == 0:
        customer_number = request.POST.get('customer_number', '')
        customer = CustomerController.getCustomerByCustomerNumber(customer_number = customer_number)
        id = customer.id
        response = JsonResponse({'id': id})
    elif id < 1:
        return redirect('customers_list')


    status      = request.COOKIES.get('customer_status_status')
    message     = request.COOKIES.get('customer_status_message')
    heartbeats  = HeartbeatController.read()

    customer    = CustomerController.getCustomerById(id = id)
    locations   = LocationController.getLocationsByCustomer(customer_id = id)
    context     = {
        'heartbeats': heartbeats,
        'locations' : locations,
        'customer'  : customer,
        'status'    : status,
        'message'   : message,
    }
    if not response:
        response = render(request, 'customers/customer.html', context = context)
        response.delete_cookie('customer_status_status')
        response.delete_cookie('customer_status_message')
    return response

def create(request: WSGIRequest) -> HttpResponse:
    heartbeats = HeartbeatController.read()
    context = {
        'title'     : 'Kunden erstellen',
        'heartbeats': heartbeats,
    }
    return render(request, 'customers/edit.html', context)

def edit(request: WSGIRequest, id: int = 0) -> HttpResponse:
    if id < 1:
        return redirect('customers_list')

    customer   = CustomerController.getCustomerById(id = id)
    heartbeats = HeartbeatController.read()
    context    = {
        'title'     : 'Kunden bearbeiten',
        'customer'  : customer,
        'heartbeats': heartbeats,
    }
    return render(request, 'customers/edit.html', context)

def save(request: WSGIRequest) -> JsonResponse:
    response = JsonResponse({})
    if request.is_ajax:
        id              = request.POST.get('id', '')
        customer_number = request.POST.get('customer_number', '')
        name            = request.POST.get('name', '')
        status          = CustomerController.save(
            id              = id,
            customer_number = customer_number,
            name            = name,
        )
        response = JsonResponse(status.__dict__)
        if status.status:
            response.set_cookie('customer_status_status' , status.status , 7)
            response.set_cookie('customer_status_message', status.message, 7)

    return response

def delete(request: WSGIRequest, id: int = 0) -> HttpResponse:
    response = redirect('customers_list')
    if id > 0:
        status = CustomerController.delete(id = id)
        response.set_cookie('customer_status_status' , status.status , 7)
        response.set_cookie('customer_status_message', status.message, 7)

    return response

def createLocation(request: WSGIRequest, customer_id: int = 0) -> HttpResponse:
    if customer_id < 1:
        return redirect('customers_list')

    heartbeats  = HeartbeatController.read()
    customer    = CustomerController.getCustomerById(id = customer_id)
    context     = {
        'title'     : 'Standort erstellen',
        'customer'  : customer,
        'heartbeats': heartbeats,
    }
    return render(request, 'customers/edit-location.html', context)

def editLocation(request: WSGIRequest, id: int = 0, customer_id: int = 0) -> HttpResponse:
    if id < 1 or customer_id < 1:
        return redirect('customers_list')

    location   = LocationController.getLocationById(id = id)
    heartbeats = HeartbeatController.read()
    customer   = CustomerController.getCustomerById(id = customer_id)
    context    = {
        'title'     : 'Standort bearbeiten',
        'location'  : location,
        'customer'  : customer,
        'heartbeats': heartbeats,
    }
    return render(request, 'customers/edit-location.html', context)

def saveLocation(request: WSGIRequest) -> JsonResponse:
    response = JsonResponse({})
    if request.is_ajax:
        id            = request.POST.get('id', '')
        name          = request.POST.get('name', '')
        email_address = request.POST.get('email_address', '')
        phone_number  = request.POST.get('phone_number', '')
        street        = request.POST.get('street', '')
        house_number  = request.POST.get('house_number', '')
        postcode      = request.POST.get('postcode', '')
        city          = request.POST.get('city', '')
        customer      = request.POST.get('customer', '')
        status        = LocationController.save(
            id            = id,
            name          = name,
            email_address = email_address,
            phone_number  = phone_number,
            street        = street,
            house_number  = house_number,
            postcode      = postcode,
            city          = city,
            customer      = customer,
        )
        response = JsonResponse(status.__dict__)
        if status.status:
            response.set_cookie('customer_status_status' , status.status , 7)
            response.set_cookie('customer_status_message', status.message, 7)

    return response

def deleteLocation(request: WSGIRequest) -> HttpResponse:
    response = JsonResponse({})
    if request.is_ajax:
        id       = request.POST.get('id', '')
        status   = LocationController.delete(id = id)
        response = JsonResponse(status.__dict__)
        response.set_cookie('customer_status_status' , status.status , 7)
        response.set_cookie('customer_status_message', status.message, 7)

    return response

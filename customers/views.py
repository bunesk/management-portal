from django.shortcuts import render, redirect
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from heartbeat.controllers import HeartbeatController
from .controllers import LocationController
from .models import Customer

def index(request: WSGIRequest) -> HttpResponse:
    return redirect('customers_list')

def customerList(request: WSGIRequest) -> HttpResponse:
    heartbeats    = HeartbeatController.read()
    customerList  = []
    for i in range(65, 91):
        char            = chr(i)
        customers       = list(Customer.objects.filter(name__startswith = char).values('id', 'name'))
        obj             = {
            'letter'   : char,
            'customers': customers,
        }
        customerList.append(obj)

    context = {
        'heartbeats': heartbeats,
        'customer_list' : customerList,
    }
    return render(request, 'customers/list.html', context=context)

def customer(request: WSGIRequest, id:int=0) -> HttpResponse:
    if id == 0:
        return redirect('customers_list')

    heartbeats  = HeartbeatController.read()
    customer    = Customer.objects.get(id = id)
    locations   = LocationController.getLocationsByCustomer(customer_id = id)
    context     = {
        'heartbeats'    : heartbeats,
        'locations'     : locations,
        'customer'      : customer,
    }
    return render(request, 'customers/customer.html', context=context)

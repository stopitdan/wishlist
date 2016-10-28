from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from . models import Product, User
from django.http import HttpResponseRedirect

# Create your views here.


def index(request):
    context={
    'myproducts':Product.objects.filter(users=User.objects.get(id=request.session['user']['id'])),
    "allproducts":Product.objects.exclude(users=User.objects.get(id=request.session['user']['id'])).exclude(join=User.objects.filter(id=request.session['user']['id'])).order_by()[::-1],
    'addedproducts':Product.objects.filter(join=User.objects.filter(id=request.session['user']['id']))
    }
    return render(request, "wishlist/index.html", context)


def addproduct(request):
    if not sessioncheck(request):
        return redirect('loginreg:index')
    return render(request, "wishlist/addproduct.html")

def createproduct(request):
    if not sessioncheck(request):
        return redirect('loginreg:index')
    validate = Product.objects.productvalidate(request.POST)
    print(validate)
    if validate:
        for error in validate:
            messages.error(request, error)
            return redirect('wishlist:addproduct')
    else:
        Product.objects.createproduct(request.POST, request.session['user']['id'])
        return redirect('wishlist:index')

def delete(request, id):
    Product.objects.get(id = id).delete()
    return redirect('wishlist:index')


def show(request, id):
    if not sessioncheck(request):
        return redirect('loginreg:index')
    context = {
    "products": Product.objects.filter(id=id)
    }
    return render(request, "wishlist/show.html", context)


def remove(request, id):
    Product.objects.delete(id,request.session['user']['id'])
    return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))


def join(request, id):
    Product.objects.join(id, request.session['user']['id'])
    return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))

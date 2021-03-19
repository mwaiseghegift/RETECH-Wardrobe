from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import  (Manufacture, Item, 
                      OrderItem, Order, 
                      WishList, WishListItem,
                      BillingAddress,
                      )
from django.utils import timezone
from .forms import ContactForm, CheckOutForm, CompletePayMent
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

import requests
from requests.auth import HTTPBasicAuth
import json
from .mpesa_credentials import MpesaAccessToken, LipaNaMpesaPassword
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def BaseView(request, *args, **kwargs):
    cart_items = Order.objects.filter(user=request.user)
    
    data = {
        'cart_items':cart_items.items.all,
    }
    return render(request, 'base.html', data)

def IndexView(request, *args, **kwargs):
    
    new_products = Item.objects.filter(date_added__lte=timezone.now()).order_by('-date_added')[:10]
    
    if request.user.is_authenticated:
        cart_items = Order.objects.filter(user=request.user)
    else:
        cart_items = 0
        
    context = {
        'manufactures': Manufacture.objects.all(),
        'new_products': new_products,
        'items':Item.objects.filter(date_added__lte=timezone.now()).order_by('-date_added'),
        'cart_items':cart_items,
    }
    return render(request, 'index.html', context)

def ContactView(request, *args, **kwargs):
    form = ContactForm()
    
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']
        form = ContactForm(request.POST)
        if form.is_valid():
            send_mail(subject, message, email, ['retechempire@gmail.com'])
            form.save()
            return HttpResponseRedirect('/contact/')
            
    context = {
        'form':form
    }
    return render(request, 'contact.html', context)

def BlogView(request, *args, **kwargs):
    context = {
        
    }
    return render(request, 'blog.html', context)

def ItemQuickView(request, slug, *args, **kwargs):
    item = get_object_or_404(Item, slug=slug)
    
    context = {
        'item',item
    }
    return render(request, 'quickviews/product-quickview.html')

def ItemDetailView(request, slug, *args, **kwargs):
    item = get_object_or_404(Item, slug=slug)
    context = {
        'item':item,
    }
    return render(request, 'product-details.html', context)

def AddToCart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(item=item,
                                                 user = request.user,
                                                 is_ordered=False
                                                 )
    order_qs = Order.objects.filter(user=request.user, is_ordered=False)
    
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "Item quantity updated")
        else:
            order.items.add(order_item)
            messages.info(request, "Item has been added to the cart")
    else:
        order = Order.objects.create(user=request.user, ordered_date=timezone.now())
        order.items.add(order_item)
        messages.info(request, "Item has been added to the cart")
    return redirect('retechecommerce:item-detail', slug=slug)

def RemoveFromCart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, is_ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(item=item,
                                                 user = request.user,
                                                 is_ordered=False
                                                 )[0]
            order.items.remove(order_item)
            messages.info(request, "Item quantity updated")
        else:
            #add some message to notify the user that the item does not exist in the cart
            messages.info(request, "The Item is not in your cart")
            return redirect('retechecommerce:item-detail', slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect('retechecommerce:item-detail', slug=slug)

@login_required    
def AddToWish(request, slug):
    item = get_object_or_404(Item, slug=slug)
    wishlist_item, created = WishListItem.objects.get_or_create(
        item=item,
        user = request.user                                                 
        )
    
    qs = WishList.objects.filter(user=request.user)
    if qs.exists():
        wishlist = qs[0]
        if wishlist.items.filter(item__slug=item.slug).exists():
            wishlist_item = WishListItem.objects.filter(
                    item=item,
                    user = request.user                                                 
                    )
            wishlist.items.remove(wishlist_item)
        else:
            wishlist = WishList.objects.create(user=request.user, timestamp=timezone.now())
            wishlist.items.add(wishlist_item)
            messages.info(request, "Item has been added to the wishlist")

    return redirect('retechecommerce:item-detail', slug=slug)

    
@login_required
def CartView(request, *args, **kwargs):
    cart_items = Order.objects.get(user=request.user, is_ordered=False) or None  
    
    total = 0
    for item in cart_items.items.all():
        total += item.totalQuantity()
    
    context = {
        'cart_items':cart_items,
        'total':total,
    }
    return render(request, 'cart.html', context)

def CheckOut(request, *args, **kwargs):
    form = CheckOutForm()
    
    if request.method == 'POST':
        form = CheckOutForm(request.POST or None)
        order = Order.objects.get(user=request.user, is_ordered=False) or None
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            tel = form.cleaned_data.get('tel')
            city = form.cleaned_data.get('city')
            address = form.cleaned_data.get('address')
            billing_address = BillingAddress(
                user = request.user,
                address = address,
                city = city,
                delivery_tel = tel,
                email = email,
            )
            billing_address.save()
            order.billing_address = billing_address
            order.save()
            return redirect('retechecommerce:checkout')
        
    context = {
        'form':form,
    }
    return render(request, 'checkout.html', context)

def PaymentView(request, *args, **kwargs):
    amount = ""
    tel = ""
    
    if request.method == 'POST':
        form = CompletePayMent(request.POST or None)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            telephone = form.cleaned_data['telephone']
            
            access_token = MpesaAccessToken.validated_mpesa_access_token
            api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
            headers = {"Authorization":"Bearer %s" % access_token}
            request = {
                "BusinessShortCode": LipaNaMpesaPassword.business_short_code,
                "Password": LipaNaMpesaPassword.decode_password,
                "Timestamp": LipaNaMpesaPassword.lipa_time,
                "TransactionType": "CustomerPayBillOnline",
                "Amount": f"{amount}",
                "PartyA": f"{telephone}",
                "PartyB": "174379",
                "PhoneNumber": f"{telephone}",
                "CallBackURL": "https://retechmall.pythonanywhere.com/saf",
                "AccountReference": "MyHealth",
                "TransactionDesc": "myhealth test"
            }
            response = requests.post(api_url, json=request, headers=headers)
            return HttpResponseRedirect('/support/checkout/')
                 
        else:
            form = CompletePayMent()
            

    
    context = {
        'amount':amount,
        'telephone':telephone,
    }
    
    return render(request, 'mpesa_checkout.html', context)
        
    

def CustomerReview(request, *args, **kwargs):
    
    context = {
        
    }
    return render(request, 'customer-review.html', context)

def Shop(request, *args, **kwargs):
    context = {
        
    }
    return render(request, 'shop.html', context)

def WishList(request, *args, **kwargs):
    context = {
        
    }
    return render(request, 'wishlist.html', context)

def Team(request, *args, **kwargs):
    context = {
        
    }
    return render(request, 'team.html', context)

def Portfolio(request, *args, **kwargs):
    context = {
        
    }
    return render(request, 'portfolio-card-box-2.html', context)

def About(request, *args, **kwargs):
    context = {
        
    }
    return render(request, 'about.html', context)

def RemoveItemFromMainCart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, is_ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(item=item,
                                                 user = request.user,
                                                 is_ordered=False
                                                 )[0]
            order.items.remove(order_item)
            messages.info(request, "Item quantity updated")
            return redirect('retechecommerce:cart')
        else:
            #add some message to notify the user that the item does not exist in the cart
            messages.info(request, "The Item is not in your cart")
            return redirect('retechecommerce:cart')
    else:
        messages.info(request, "You do not have an active order")
        return redirect('retechecommerce:cart')
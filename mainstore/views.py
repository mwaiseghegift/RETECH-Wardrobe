from django.shortcuts import render, get_object_or_404, redirect, HttpResponse, reverse
from django.utils import timezone
from .models import  (Manufacture, Item, 
                      OrderItem, Order, 
                      WishListItem, UserWishList,
                      BillingAddress, Payment, Coupon, Category, MpesaPayment
                      )
from blog.models import Blog
from accounts.models import Staff
from django.http import JsonResponse

from django.utils import timezone
from .forms import ContactForm, CheckOutForm, CompletePayMent, CouponForm
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

import requests
from requests.auth import HTTPBasicAuth
import json
from .mpesa_credentials import MpesaAccessToken, LipaNaMpesaPassword
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

from django.core.exceptions import ObjectDoesNotExist
# Create your views here.

def BaseView(request, *args, **kwargs):
    cart_items = Order.objects.filter(user=request.user)
    
    data = {
        'cart_items':cart_items,
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
        'news':Blog.objects.filter(is_published=True).order_by('-pub_date')[:3]
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
            send_mail(subject, message, email, ['retechempire@gmail.com'], fail_silently=True)
            form.save()
            return HttpResponseRedirect('/contact/')
            
    context = {
        'form':form
    }
    return render(request, 'contact.html', context)


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
    wishlist_item, created = WishListItem.objects.get_or_create(item=item,
                                                user=request.user
                                                )
    wishlist_qs = UserWishList.objects.filter(user=request.user)
    
    if wishlist_qs.exists():
        wishlist = wishlist_qs[0]
        if wishlist.items.filter(item__slug=item.slug).exists():
            messages.info(request, 'Item is already in the cart')
            return redirect('retechecommerce:item-detail', slug=slug)
        else:
            wishlist.items.add(wishlist_item)
            messages.info(request, "Item added to the wishlist")
            return redirect('retechecommerce:item-detail', slug=slug)
    else:
        wishlist = UserWishList.objects.create(user=request.user,
                                            timestamp = timezone.now()
                                            )
        wishlist.items.add(wishlist_item)
        messages.info(request, "Item added to the cart")
        return redirect('retechecommerce:item-detail', slug=slug)
    return redirect('retechecommerce:item-detail', slug=slug)

def RemoveItemFromWishList(request, slug):
    item = get_object_or_404(Item, slug=slug)
    wishlist_qs = UserWishList.objects.filter(user=request.user)
    if wishlist_qs.exists():
        wishlist = wishlist_qs[0]
        if wishlist.items.filter(item__slug=item.slug).exists():
            wishlist_item = WishListItem.objects.filter(item=item,
                                                 user = request.user
                                                 )[0]
            wishlist.items.remove(wishlist_item)
            messages.info(request, "Item was removed from cart")
            return redirect('retechecommerce:wishlist')
        else:
            #add some message to notify the user that the item does not exist in the cart
            messages.info(request, "The Item is not in wishlist")
            return redirect('retechecommerce:wishlist')
    
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

def getAccessToken(request):
    consumer_key = 'zy4Z7vfCxfdllh62bGoyMK9trPUPGC16'
    consumer_secret = 'hbUrTs79dLniTQlW'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    
    r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token['access_token']
    
    return HttpResponse(validated_mpesa_access_token)

@login_required
def LipaNaMpesaView(request, *args, **kwargs):
    order = Order.objects.get(user=request.user, is_ordered=False)
    amount = order.totalPrice()
    telephone = ""
    
    if request.method == 'POST':
        telephone = request.POST['phone-no']
        
       
            
        print(telephone)
        
        access_token = MpesaAccessToken.validated_mpesa_access_token
        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {"Authorization":"Bearer %s" % access_token}
        request = {
            "BusinessShortCode": LipaNaMpesaPassword.business_short_code,
            "Password": LipaNaMpesaPassword.decode_password,
            "Timestamp": LipaNaMpesaPassword.lipa_time,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": "5",
            "PartyA": f"254{telephone}",
            "PartyB": "174379",
            "PhoneNumber": f"254{telephone}",
            "CallBackURL": "https://retechmall.pythonanywhere.com/saf",
            "AccountReference": "Retech Store",
            "TransactionDesc": "Retech Store Test"
        }
        response = requests.post(api_url, json=request, headers=headers)
        return HttpResponseRedirect(reverse('retechecommerce:lipa-na-mpesa'))
                
    else:
        form = CompletePayMent()
            

    
    context = {
        'amount':amount,
        'telephone':telephone,
    }
    
    return render(request, 'payments/mpesa_checkout.html', context)
 

      
    
#register confirmation and validation url with safaricom
@csrf_exempt
def register_urls(request):
    access_token = MpesaAccessToken.validated_mpesa_access_token
    api_url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"
    headers = {"Authorization":"Bearer %s" % access_token}
    options = {"ShortCode": LipaNaMpesaPassword.business_short_code,
               "ResponseType":"Completed",
               "ConfirmationUrl":"https://5590a37a7745.ngrok.io/c2b/confirmation",
               "ValidationUrl": "https://5590a37a7745.ngrok.io/c2b/validation",
               }
    response = requests.post(api_url, json=options, headers=headers)
    return HttpResponse(response.text)

#capture the mpesa calls
@csrf_exempt
def call_back(request):
    pass

@csrf_exempt
def validation(request):
    context = {
        "ResultCode":0,
        "ResultDesc":"Accepted"
    }
    return JsonResponse(dict(context))

@csrf_exempt
def confirmation(request):
    mpesa_body = request.body.decode('utf-8')
    mpesa_payment = json.loads(mpesa_body)
    
    payment = MpesaPayment (
        first_name = mpesa_payment['FirstName'],
        last_name = mpesa_payment['LastName'],
        middle_name = mpesa_payment['MiddleName'],
        description = mpesa_payment['TransID'],
        phone_number = mpesa_payment['MSISDN'],
        amount = mpesa_payment['TransAmount'],
        reference = mpesa_payment['BillRefNumber'],
        organization_balance = mpesa_payment['OrgAccountBalance'],
        type = mpesa_payment['TransactionType']
    )
    payment.save()
    context = {
        "ResultCode":0,
        "ResultDesc":"Accepted"
    }
    
    return JsonResponse(dict(context))

def CustomerReview(request, *args, **kwargs):
    
    context = {
        
    }
    return render(request, 'customer-review.html', context)

def Shop(request, *args, **kwargs):
    shop_items = Item.objects.filter(date_added__lte=timezone.now()).order_by('-date_added')
    context = {
        'shop_items':shop_items,
    }
    return render(request, 'shop.html', context)

def WishList(request, *args, **kwargs):
    
    wish_items = get_object_or_404(UserWishList, user=request.user )
    
    context = {
        'items':wish_items.items.all()
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
        'staff':Staff.objects.all(),    
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
    

def get_coupon(request, code):
    try:
        coupon = Coupon.objects.get(code=code)
        return coupon
    except ObjectDoesNotExist:
        messages.info(request, "The coupon does not exist")
        return redirect('retechecommerce:checkout')
 
def AddCoupon(request):
    if request.method == 'POST':
        form = ContactForm(request.POST or None)
        if form.is_valid(): 
            try:
                code = form.cleaned_data.get('code')
                order = Order.objects.get(user=request.user, is_ordered=False)
                coupon = get_coupon(request, code)
            except ObjectDoesNotExist:
                messages.info(request, "You do not have an active order")
                return redirect('retechecommerce:checkout')
            
def ItemCategoryView(request, slug):
    category = get_object_or_404(Category, slug=slug)
    category_items = category.CategoryItems()
    
    context = {
        'shop_items':category_items,
    }
    return render(request, 'category.html', context)

def ItemSearchResults(request, *args, **kwargs):
    items = Item.objects.filter(date_added__lte=timezone.now()).order_by('-date_added')
    
    query = request.GET.get('q', None)
    
    if query is not None:
        items = Item.objects.filter(Q(name__icontains=query))
                                    
        
    context = {
        'shop_items':items,
        'query':query,
    }
    return render(request, 'search-results.html', context)
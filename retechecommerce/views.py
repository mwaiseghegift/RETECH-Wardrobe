from django.shortcuts import render
from django.utils import timezone
from .models import  Manufacture, Item

# Create your views here.

def IndexView(request, *args, **kwargs):
    
    new_products = Item.objects.filter(date_added__lte=timezone.now()).order_by('-date_added')[:8]
    
    context = {
        'manufactures': Manufacture.objects.all(),
        'new_products': new_products,
    }
    return render(request, 'index.html', context)

def ContactView(request, *args, **kwargs):
    context = {
        
    }
    return render(request, 'contact.html', context)

def BlogView(request, *args, **kwargs):
    context = {
        
    }
    return render(request, 'blog.html', context)

def BlogDetailView(request, slug, *args, **kwargs):
    context = {
        
    }
    return render(request, 'blog-detail.html', context)

def CartView(request, *args, **kwargs):
    context = {
        
    }
    return render(request, 'cart.html', context)

def CheckOut(request, *args, **kwargs):
    context = {
        
    }
    return render(request, 'checkout.html', context)

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
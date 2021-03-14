from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import  Manufacture, Item

from .forms import ContactForm
from django.core.mail import send_mail
from django.http import HttpResponseRedirect

# Create your views here.

def IndexView(request, *args, **kwargs):
    
    new_products = Item.objects.filter(date_added__lte=timezone.now()).order_by('-date_added')[:10]
    context = {
        'manufactures': Manufacture.objects.all(),
        'new_products': new_products,
        'items':Item.objects.filter(date_added__lte=timezone.now()).order_by('-date_added')
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

def ItemDetailView(request, slug, *args, **kwargs):
    item = get_object_or_404(Item, slug=slug)
    context = {
        'item':Item,
    }
    return render(request, 'item-details.html', context)

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
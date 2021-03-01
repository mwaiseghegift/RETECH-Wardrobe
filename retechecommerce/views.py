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

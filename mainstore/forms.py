from django import forms
from .models import Contact

class ContactForm(forms.ModelForm):
    
    class Meta:
        model = Contact
        fields = ['name','email','subject','message']
        
class CheckOutForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    tel = forms.CharField()
    city = forms.CharField()
    address = forms.CharField()
    
class CompletePayMent(forms.Form):
    tel = forms.CharField()
    amount = forms.DecimalField(max_digits=10)
    
    

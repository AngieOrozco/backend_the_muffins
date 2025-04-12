from django import forms 
from .models import Auction 

class AuctionForm(forms.ModelForm): 
    class Meta: 
        model = Auction 
        fields = [ 
        'title', 'description', 'price', 'discount_percentage',  
        'rating', 'stock', 'brand', 'category', 'thumbnail' 
        ] 
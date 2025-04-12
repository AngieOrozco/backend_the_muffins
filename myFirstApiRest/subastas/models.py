from django.db import models
from django.core.validators import MinValueValidator 
from django.core.validators import MaxValueValidator 
# Create your models here.

from django.db import models 
 
class Category(models.Model): 
    name = models.CharField(max_length=50, blank=False, unique=True) 
 
    class Meta:  
        ordering=('id',)  
 
    def __str__(self): 
        return self.name 
 
class Auction(models.Model): 
    title = models.CharField(max_length=150) 
    description = models.TextField() 
    price = models.DecimalField(max_digits=10, decimal_places=2) 
    rating = models.DecimalField(max_digits=3, decimal_places=2, validators=[MinValueValidator(1), MaxValueValidator(5)]) 
    stock = models.IntegerField(validators=[MinValueValidator(1)]) 
    brand = models.CharField(max_length=100) 
    category = models.ForeignKey(Category, related_name='auctions', on_delete=models.CASCADE) 
    thumbnail = models.URLField() 
    creation_date = models.DateTimeField(auto_now_add=True)      
    closing_date = models.DateTimeField() 
 
    class Meta:  
        ordering=('id',)  

class Bid(models.Model):
    auction = models.ForeignKey(Auction, related_name='bids', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    bidder = models.CharField(max_length=100)  # nombre o identificador del que puja
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-timestamp',)

    def __str__(self):
        return f"{self.bidder} - {self.amount}€"
 
    def __str__(self): 
        return self.title 




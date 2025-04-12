from django.db import models

# Create your models here.
from django.db import models 

class Auction(models.Model): 
    title = models.CharField(max_length=150) 
    description = models.TextField() 
    price = models.DecimalField(max_digits=10, decimal_places=2) 
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2) 
    rating = models.DecimalField(max_digits=3, decimal_places=2) 
    stock = models.IntegerField() 
    brand = models.CharField(max_length=100) 
    category = models.CharField(max_length=50) 
    thumbnail = models.URLField() 

def __str__(self): 
    return self.title 

from django.db import models
from django.core.validators import MinValueValidator 
from django.core.validators import MaxValueValidator 
from django.utils import timezone 
from django.contrib.auth.models import AbstractUser
from django.db import models
# Create your models here.
from users.models import CustomUser 
from django.db.models import Avg


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
    auctioneer = models.ForeignKey(CustomUser, related_name='auctions', 
    on_delete=models.CASCADE) 
 
    class Meta:  
        ordering=('id',)  
        
    def __str__(self): 
        return self.title 

    def average_rating(self):
        avg = self.ratings.aggregate(Avg('score'))['score__avg']
        return round(avg, 2) if avg else 1

class Bid(models.Model):
    auction = models.ForeignKey(Auction, related_name='bids', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    bidder = models.ForeignKey(CustomUser, related_name='bids', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-timestamp',)

    def __str__(self):
        return f"{self.bidder} - {self.amount}€"
 
    def __str__(self): 
        return self.title 

class Rating(models.Model):
    score = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    user = models.ForeignKey(CustomUser, related_name='ratings', on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, related_name='ratings', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'auction')  # cada usuario puede valorar solo una vez

    def __str__(self):
        return f"{self.user} → {self.auction} = {self.score}"

class Comment(models.Model):
    title = models.CharField(max_length=150)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(CustomUser, related_name='comments', on_delete=models.CASCADE)
    auction = models.ForeignKey('Auction', related_name='comments', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} - {self.user.username}"




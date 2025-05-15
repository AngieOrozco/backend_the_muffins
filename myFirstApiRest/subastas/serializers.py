from rest_framework import serializers 
from .models import Category, Auction 
from django.utils import timezone 
from .models import Bid
from drf_spectacular.utils import extend_schema_field 
from .models import Rating

class CategoryListCreateSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Category 
        fields = ['id','name'] 

class CategoryDetailSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Category 
        fields = '__all__' 



class AuctionListCreateSerializer(serializers.ModelSerializer): 
    creation_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ", read_only=True)
    closing_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ")
    isOpen = serializers.SerializerMethodField(read_only=True)
    auctioneer = serializers.ReadOnlyField(source='auctioneer.id') 

    class Meta: 
        model = Auction 
        fields = '__all__'
        
    @extend_schema_field(serializers.BooleanField())
    def get_isOpen(self, obj): 
        return obj.closing_date > timezone.now()


    def validate_closing_date(self, value): 
        # Validar que la fecha de cierre sea mayor que la fecha actual
        if value <= timezone.now():
            raise serializers.ValidationError("Closing date must be greater than now.")
        
        # Obtener la fecha de creación; si no existe (al crear la subasta), usar timezone.now()
        creation_date = self.instance.creation_date if self.instance else timezone.now()

        # Validar que la diferencia entre las fechas sea de al menos 15 días
        minimum_closing_date = creation_date + timezone.timedelta(days=15)
        if value < minimum_closing_date:
            raise serializers.ValidationError(
                f"Closing date must be at least 15 days after the creation date (minimum: {minimum_closing_date})."
            )
        
        return value

class AuctionDetailSerializer(serializers.ModelSerializer): 

    creation_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ", read_only=True) 

    closing_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ") 

    isOpen = serializers.SerializerMethodField(read_only=True) 
    auctioneer = serializers.ReadOnlyField(source='auctioneer.id')
    average_rating = serializers.SerializerMethodField()

    class Meta: 
        model = Auction 
        fields = '__all__'
    
    @extend_schema_field(serializers.BooleanField()) 
    def get_isOpen(self, obj): 
        return obj.closing_date > timezone.now() 

    def validate_closing_date(self, value): 
        if value <= timezone.now(): 
            raise serializers.ValidationError("Closing date must be greater than now.") 
        return value 

    def get_average_rating(self, obj):
        return obj.average_rating()

class BidSerializer(serializers.ModelSerializer):
    timestamp = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ", read_only=True)
    bidder = serializers.ReadOnlyField(source='bidder.id')
    auction = serializers.ReadOnlyField(source='auction.id')

    class Meta:
        model = Bid
        fields = '__all__'

    def validate(self, data):
        auction = data.get("auction")
        amount = data.get("amount")

        # Obtener la puja más alta actual
        highest_bid = Bid.objects.filter(auction=auction).order_by('-amount').first()
        if highest_bid and amount <= highest_bid.amount:
            raise serializers.ValidationError("The bid must be higher than the current highest bid.")
        return data


class RatingSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')
    auction = serializers.ReadOnlyField(source='auction.id')

    class Meta:
        model = Rating
        fields = '__all__'

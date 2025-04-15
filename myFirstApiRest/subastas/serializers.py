from rest_framework import serializers 
from .models import Category, Auction 
from django.utils import timezone 

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

    class Meta: 
        model = Auction 
        fields = '__all__'

    def get_isOpen(self, obj): 
        return obj.closing_date > timezone.now()
    
    def validate_closing_date(self, value): 
        if value <= timezone.now(): 
            raise serializers.ValidationError("Closing date must be greater than now.") 
        return value

    def validate(self, data):
        closing_date = data.get('closing_date')

        # Si es una edición (instancia ya existe), usa su fecha de creación original
        creation_date = self.instance.creation_date if self.instance else timezone.now()

        if closing_date and closing_date <= creation_date + timezone.timedelta(days=15):
            raise serializers.ValidationError({
                "closing_date": "La fecha de cierre debe ser al menos 15 días posterior a la fecha de creación."
            })
        return data

    



class AuctionDetailSerializer(serializers.ModelSerializer): 

    creation_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ", read_only=True) 

    closing_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ") 

    isOpen = serializers.SerializerMethodField(read_only=True) 

    class Meta: 
        model = Auction 
        fields = '__all__'
    
    def get_isOpen(self, obj): 
        return obj.closing_date > timezone.now() 

    def validate_closing_date(self, value): 
        if value <= timezone.now(): 
            raise serializers.ValidationError("Closing date must be greater than now.") 
        return value

    def validate(self, data):
        closing_date = data.get('closing_date')

        # Si es una edición (instancia ya existe), usa su fecha de creación original
        creation_date = self.instance.creation_date if self.instance else timezone.now()

        if closing_date and closing_date <= creation_date + timezone.timedelta(days=15):
            raise serializers.ValidationError({
                "closing_date": "La fecha de cierre debe ser al menos 15 días posterior a la fecha de creación."
            })
        return data


<<<<<<< Updated upstream
=======
    class Meta:
        model = Bid
        fields = '__all__'

    def validate(self, data):
        auction = data.get("auction")
        amount = data.get("amount")

        if auction.closing_date <= timezone.now():
            raise serializers.ValidationError("The auction is closed. You cannot place a bid.")

        highest_bid = Bid.objects.filter(auction=auction).order_by('-amount').first()
        if highest_bid and amount <= highest_bid.amount:
            raise serializers.ValidationError(
                f"La puja debe ser superior a la última puja (actual: {highest_bid.amount}€)."
            )

        return data
>>>>>>> Stashed changes

from django.shortcuts import render
from django.db.models import Q 
from drf_spectacular.utils import extend_schema

# Create your views here.
from rest_framework import generics 
from .models import Category, Auction 
from .serializers import CategoryListCreateSerializer, CategoryDetailSerializer, AuctionListCreateSerializer, AuctionDetailSerializer 

class CategoryListCreate(generics.ListCreateAPIView): 
    queryset = Category.objects.all() 
    serializer_class = CategoryListCreateSerializer 

class CategoryRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView): 
    queryset = Category.objects.all() 
    serializer_class = CategoryDetailSerializer 

class AuctionListCreate(generics.ListCreateAPIView): 
    queryset = Auction.objects.all() 
    serializer_class = AuctionListCreateSerializer 

    def get_queryset(self): 
        queryset = Auction.objects.all() 
        params = self.request.query_params 

        search = params.get('search', None) 
        if search and len(search) < 3: 
            raise ValidationError( 
            {"search": "Search query must be at least 3 characters long."}, 
            code=status.HTTP_400_BAD_REQUEST 
            ) 
        if search:
            queryset =  queryset.filter(Q(title__icontains=search) | 
                Q(description__icontains=search))
        # Filtro por categoría
        category_id = params.get('categoria', None)
        if category_id:
            if not Category.objects.filter(id=category_id).exists():
                raise ValidationError(
                    {"categoria": "Category ID does not exist in the database."},
                    code=status.HTTP_400_BAD_REQUEST
                )
            queryset = queryset.filter(category_id=category_id)

        # Filtro por rango de precios
        price_min = params.get('price_min', None)
        price_max = params.get('price_max', None)

        # Validaciones de precio
        if price_min:
            try:
                price_min = int(price_min)
                if price_min < 1:
                    raise ValidationError({"price_min": "Price must be a positive number."})
            except ValueError:
                raise ValidationError({"price_min": "Invalid price format. Must be a number."})

        if price_max:
            try:
                price_max = int(price_max)
                if price_max < 1:
                    raise ValidationError({"price_max": "Price must be a positive number."})
            except ValueError:
                raise ValidationError({"price_max": "Invalid price format. Must be a number."})

        if price_min and price_max and price_max <= price_min:
            raise ValidationError({"price_range": "Maximum price must be greater than minimum price."})

        # Aplicar los filtros de precios si están presentes
        if price_min:
            queryset = queryset.filter(price__gte=price_min)
        if price_max:
            queryset = queryset.filter(price__lte=price_max)      
        return queryset 

class AuctionRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView): 
    queryset = Auction.objects.all() 
<<<<<<< Updated upstream
    serializer_class = AuctionDetailSerializer
=======
    serializer_class = AuctionDetailSerializer

@extend_schema(
    summary="Lista y creación de pujas para una subasta",
    description="Devuelve todas las pujas asociadas a una subasta o permite crear una nueva puja."
)

class BidListCreate(generics.ListCreateAPIView):
    serializer_class = BidSerializer

    def get_queryset(self):
        auction_id = self.kwargs['auction_id']
        return Bid.objects.filter(auction_id=auction_id)

    def perform_create(self, serializer):
        auction_id = self.kwargs['auction_id']
        serializer.save(auction_id=auction_id)

class BidRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BidSerializer

    def get_queryset(self):
        auction_id = self.kwargs['auction_id']
        return Bid.objects.filter(auction_id=auction_id)
    
    def get_object(self):
        obj = super().get_object()
        if obj.auction.closing_date <= timezone.now():
            raise ValidationError("Cannot modify or delete a bid from a closed auction.")
        return obj
>>>>>>> Stashed changes

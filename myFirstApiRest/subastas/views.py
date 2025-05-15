from django.shortcuts import render
from django.db.models import Q 
# Create your views here.
from rest_framework import generics, status 
from .models import Category, Auction, Bid 
from .serializers import CategoryListCreateSerializer, CategoryDetailSerializer, AuctionListCreateSerializer, AuctionDetailSerializer, BidSerializer 
from rest_framework.exceptions import ValidationError 
from rest_framework.views import APIView 
from rest_framework.permissions import IsAuthenticated 
from rest_framework.response import Response
from .permissions import IsOwnerOrAdmin 
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from users.permissions import IsAdminOrReadOnly, IsOwnerOrAdmin
from .models import Rating
from .serializers import RatingSerializer

class CategoryListCreate(generics.ListCreateAPIView): 
    #permission_classes = [IsAdminOrReadOnly]

    queryset = Category.objects.all() 
    serializer_class = CategoryListCreateSerializer 

class CategoryRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView): 
    permission_classes = [IsAdminOrReadOnly]

    queryset = Category.objects.all() 
    serializer_class = CategoryDetailSerializer 

class AuctionListCreate(generics.ListCreateAPIView): 
    permission_classes = [IsAuthenticatedOrReadOnly]

    queryset = Auction.objects.all() 
    serializer_class = AuctionListCreateSerializer 

    def perform_create(self, serializer):
        print("🚀 Usuario autenticado:", self.request.user)
        serializer.save(auctioneer=self.request.user)

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
        category_id = params.get('category', None)
        if category_id:
            if not Category.objects.filter(id=category_id).exists():
                raise ValidationError(
                    {"category": "Category ID does not exist in the database."},
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
    #permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrAdmin]  
    queryset = Auction.objects.all() 
    serializer_class = AuctionDetailSerializer

    def perform_update(self, serializer):
        serializer.save(auctioneer=self.request.user)

class BidListCreate(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    serializer_class = BidSerializer

    def get_queryset(self):
        auction_id = self.kwargs['auction_id']
        return Bid.objects.filter(auction_id=auction_id)

    def perform_create(self, serializer):
        auction_id = self.kwargs['auction_id']
        serializer.save(auction_id=auction_id, bidder=self.request.user)


class BidRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    #permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = BidSerializer

    def get_queryset(self):
        auction_id = self.kwargs['auction_id']
        return Bid.objects.filter(auction_id=auction_id)
    
    def perform_create(self, serializer):
        auction_id = self.kwargs['auction_id']
        serializer.save(auction_id=auction_id, bidder=self.request.user)
    
class UserAuctionListView(APIView): 
    permission_classes = [IsAuthenticated] 
    def get(self, request, *args, **kwargs): 
        # Obtener las subastas del usuario autenticado 
        user_auctions = Auction.objects.filter(auctioneer=request.user) 
        serializer = AuctionListCreateSerializer(user_auctions, many=True) 
        return Response(serializer.data) 
    


class RatingListCreateUpdateDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, auction_id):
        score = request.data.get('score')
        if not score:
            return Response({'detail': 'Score is required'}, status=400)
        
        try:
            rating, created = Rating.objects.update_or_create(
                user=request.user,
                auction_id=auction_id,
                defaults={'score': score}
            )
            return Response(RatingSerializer(rating).data)
        except Exception as e:
            return Response({'detail': str(e)}, status=400)

    def delete(self, request, auction_id):
        Rating.objects.filter(user=request.user, auction_id=auction_id).delete()
        return Response({'detail': 'Rating deleted'}, status=204)

from django.shortcuts import render

# Create your views here.

from rest_framework import status, generics 
from rest_framework.response import Response 
from rest_framework_simplejwt.tokens import RefreshToken 
from .models import CustomUser 
from .serializers import UserSerializer, ChangePasswordSerializer
from rest_framework.exceptions import ValidationError 
from django.contrib.auth.password_validation import validate_password 

from rest_framework.views import APIView 
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser 
from django.contrib.auth import authenticate
from subastas.models import Auction, Bid
from subastas.serializers import AuctionListCreateSerializer, BidSerializer

class LogoutView(APIView): 
    permission_classes = [IsAuthenticated]
    def post(self, request): 
        """Realiza el logout eliminando el RefreshToken (revocar)""" 
        try: 
            # Obtenemos el RefreshToken del request  
            #Se esperan que esté en el header Authorization 
            refresh_token = request.data.get('refresh', None) 
            if not refresh_token: 
                return Response({"detail": "No refresh token provided."}, status=status.HTTP_400_BAD_REQUEST) 
 
            # Revocar el RefreshToken 
            token = RefreshToken(refresh_token) 
            token.blacklist()   
            return Response({"detail": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT) 
 
        except Exception as e: 
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST) 
        
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'username': user.username
            })
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class UserRegisterView(generics.CreateAPIView): 
    permission_classes = [AllowAny]
    queryset = CustomUser.objects.all() 
    serializer_class = UserSerializer 
 
    def create(self, request, *args, **kwargs): 
        serializer = self.get_serializer(data=request.data) 
        if serializer.is_valid(): 
            user = serializer.save() 
            refresh = RefreshToken.for_user(user) 
            return Response({ 
                'user': serializer.data, 
                'access': str(refresh.access_token), 
                'refresh': str(refresh), 
            }, status=status.HTTP_201_CREATED) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
 
class UserListView(generics.ListAPIView): 
    permission_classes = [IsAdminUser] 
    serializer_class = UserSerializer 
    queryset = CustomUser.objects.all() 
 
class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView): 
    permission_classes = [IsAdminUser]
    serializer_class = UserSerializer 
    queryset = CustomUser.objects.all() 

class UserProfileView(APIView): 
    permission_classes = [IsAuthenticated] 
    def get(self, request): 
        serializer = UserSerializer(request.user) 
        return Response(serializer.data) 
 
    def patch(self, request): 
        serializer = UserSerializer(request.user, data=request.data, partial=True) 
        if serializer.is_valid(): 
            serializer.save() 
            return Response(serializer.data) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
 
    def delete(self, request): 
        user = request.user 
        user.delete() 
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class ChangePasswordView(APIView): 
    permission_classes = [IsAuthenticated] 
    def post(self, request): 
        serializer = ChangePasswordSerializer(data=request.data) 
        user = request.user 
 
        if serializer.is_valid(): 
            if not user.check_password(serializer.validated_data['old_password']): 
                return Response({"old_password": "Incorrect current password."}, 
                                status=status.HTTP_400_BAD_REQUEST) 
 
            try: 
                validate_password(serializer.validated_data['new_password'], user) 
            except ValidationError as e: 
                return Response({"new_password": e.messages}, status=status.HTTP_400_BAD_REQUEST) 
 
            user.set_password(serializer.validated_data['new_password']) 
            user.save() 
            return Response({"detail": "Password updated successfully."}) 
 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class MisSubastasView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        subastas = Auction.objects.filter(auctioneer=request.user)
        serializer = AuctionListCreateSerializer(subastas, many=True)
        return Response(serializer.data)

class MisPujasView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        pujas = Bid.objects.filter(bidder=request.user)
        serializer = BidSerializer(pujas, many=True)
        return Response(serializer.data)
    
def perform_create(self, serializer):
    auction_id = self.kwargs['auction_id']
    serializer.save(auction_id=auction_id, bidder=self.request.user)

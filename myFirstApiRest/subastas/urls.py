from django.urls import path
from .views import (
    CategoryListCreate, CategoryRetrieveUpdateDestroy,
    AuctionListCreate, AuctionRetrieveUpdateDestroy,
    BidListCreate, BidRetrieveUpdateDestroy, UserAuctionListView, RatingListCreateUpdateDeleteView
)

app_name = "subastas"

urlpatterns = [
    # Categorías
    path('categorias/', CategoryListCreate.as_view(), name='categoria-list-create'),
    path('categoria/<int:pk>/', CategoryRetrieveUpdateDestroy.as_view(), name='categoria-detail'),

    # Subastas
    path('', AuctionListCreate.as_view(), name='subasta-list-create'),
    path('<int:pk>/', AuctionRetrieveUpdateDestroy.as_view(), name='subasta-detail'),

    # Pujas
    path('<int:auction_id>/pujas/', BidListCreate.as_view(), name='puja-list-create'),
    path('<int:auction_id>/pujas/<int:pk>/', BidRetrieveUpdateDestroy.as_view(), name='puja-detail'),

    path('users/', UserAuctionListView.as_view(), name='action-from-users'), 
    path('subastas/<int:auction_id>/rating/', RatingListCreateUpdateDeleteView.as_view()),

]

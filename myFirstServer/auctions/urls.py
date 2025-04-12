
from django.urls import path 
from .views import hello_view, index, detail, create, edit
urlpatterns = [ 
path('hello/', hello_view, name='hello'), 
path("", index, name="index"), 
path("<int:auction_id>", detail, name="detail"), 
path('new/', create, name='create'), 
path('edit/', edit, name = 'edit'),
] 
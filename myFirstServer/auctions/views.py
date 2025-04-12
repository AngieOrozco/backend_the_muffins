

# Create your views here.
from django.http import HttpResponse 
from django.template import loader 
from django.shortcuts import render , redirect
from .models import Auction 
from .forms import AuctionForm

def hello_view(request): 
    name = request.GET.get('name', 'World') 
    subject = request.GET.get('subject', 'DAS') 
    date = request.GET.get('date', '14')
    date= int(date)
    return render(request, 'auctions/hello.html', {'name': name , 'subject': subject, 'date': date})

def index(request): 
    auctions = Auction.objects.all() 
    template = loader.get_template("auctions/index.html") 
    context = { "auction_list": auctions } 
    return HttpResponse(template.render(context, request)) 
def detail(request, auction_id): 
    auction = Auction.objects.get(id=auction_id)   
    context = { "auction": auction } 

    return render(request, "auctions/detail.html", context)

def create(request): 
    if request.method == "POST": 
        form = AuctionForm(request.POST) 
        if form.is_valid(): 
            form.save() 
            return redirect('index')  
    else: 
        form = AuctionForm() 

    return render(request, 'auctions/new.html', {'form': form}) 

def edit(request):
    if request.method == "POST":
        form = Auc
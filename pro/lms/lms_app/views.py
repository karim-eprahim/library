from multiprocessing import context
from django.shortcuts import get_object_or_404, redirect, render
from .models import *
from .forms import Bookform, Categoryform

# Create your views here.


def index(request):
    if request.method == 'POST':
        add_book = Bookform(request.POST, request.FILES)
        if add_book.is_valid():
            add_book.save()

        add_category = Categoryform(request.POST)
        if add_category.is_valid():
            add_category.save()
    context = {
        'books':Book.objects.all(),
        'category':Category.objects.all(),
        'form': Bookform(),
        'formcat':Categoryform(),
        'allbooks':Book.objects.filter(active=True).count(),   
        'booksolid':Book.objects.filter(status='sold').count(),
        'bookrental':Book.objects.filter(status='rental').count(),
        'bookavailable':Book.objects.filter(status='available').count(),
    }
    return render(request, 'pages/index.html', context)

def books(request):

    search = Book.objects.all()
    title = None
    if 'search_name' in request.GET:
        title = request.GET['search_name']
        if title:
            search = search.filter(title__icontains = title)


    context = {
        'books':search,
        'category':Category.objects.all(),
        'formcat':Categoryform(),
    }
    return render(request, 'pages/books.html' ,context)

def update(request, id):
    book_id = Book.objects.get(id=id)
    if request.method == 'POST':
        book_save = Bookform(request.POST, request.FILES, instance=book_id)
        if book_save.is_valid():
            book_save.save()
            return redirect('/')
    else:
        book_save = Bookform(instance=book_id)  
    context = {
        'form':book_save,
    }          
    return render(request, 'pages/update.html', context)


def delete(request, id):
    book_delete = get_object_or_404(Book, id=id)
    if request.method == 'POST':
        book_delete.delete()
        return redirect('/')
    return render(request, 'pages/delete.html')    
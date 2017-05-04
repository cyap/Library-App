from django.shortcuts import render
from django.template import RequestContext

from .forms import BookForm

# Create your views here.

def index(request):
	book_form = BookForm()
	return render(request, "index.html", {
			"book_form":book_form
		})

def add(request):
	return

def delete(request):
	return

def edit(request):
	return
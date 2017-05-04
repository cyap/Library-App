from django.shortcuts import render
from django.template import RequestContext
from django.http import JsonResponse

from .forms import BookForm
from .models import Book, Transaction

def index(request):
	book_form = BookForm()
	return render(request, "index.html", {
		"book_form":book_form
	})

def books(request):
	# Query the database for list of books
	books = list(Book.objects.all())

	# Sample book while database is empty
	books = [{
		"isbn": 100001,
		"title": "Test2",
		"author": "Author2",
		"published": 1998,
		"genre": "Western",
		"stock": 3,
		"issued": 0
	}]

	# Return as JSON objects
	return JsonResponse(data={"books":books})

def add(request):
	return

def delete(request):
	return

def edit(request):
	return
from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponse, JsonResponse
from django.core import serializers

import json

from .forms import BookForm
from .models import Book, Transaction

def index(request):
	book_form = BookForm()
	return render(request, "index.html", {
		"book_form":book_form
	})

def books(request):
	# Query the database for list of books
	book_list = list(Book.objects.all())

	# Sample book while database is empty
	book_list = [{
	"fields": {
		"isbn": 100001,
		"title": "Test2",
		"author": "Author2",
		"published": 1998,
		"genre": "Western",
		"stock": 3,
		"issued": 0
		}
	}]

	# Return as JSON objects
	return JsonResponse(data={"books":book_list})

def add(request):
	book = Book(**json.loads(request.body))
	# TODO: Save book to database
	book_list = serializers.serialize("json", [book])

	# TODO: Load books from database, in order from most recent to least
	# book_list = list(Book.objects.all())

	return JsonResponse(data={"books":book_list})

def delete(request):
	return

def edit(request):
	return
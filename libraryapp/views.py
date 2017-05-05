from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponse, JsonResponse
from django.core import serializers

import json

from .forms import BookForm
from .models import Book, Transaction

def index(request):
	return render(request, "index.html", {
		"book_form":BookForm()
	})

def books(request):
	# Query the database for list of books
	book_list = serializers.serialize("json", Book.objects.all()[::-1])

	# Return as JSON objects
	return JsonResponse(data={"books":book_list})

def add(request):
	book = Book(**json.loads(request.body))
	book.issued = 0
	try:
		book.save()
	except:
		# TODO: Duplicate ISBN: Render error in template
		pass

	return books(request)

def delete(request):
	# Use ISBN as id, since ISBN should be unique
	book = Book.objects.get(isbn=int(json.loads(request.body)["isbn"]))
	book.delete()
	return books(request)
	return JsonResponse(data={"books":book_list})

def edit(request):
	return
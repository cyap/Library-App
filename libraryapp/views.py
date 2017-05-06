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

def books(request, errors={}):
	# Query the database for list of books
	book_list = serializers.serialize("json", Book.objects.all()[::-1])

	# Return as JSON objects
	return JsonResponse(data={"books":book_list, "errors":errors})

def add(request):
	book = Book(**json.loads(request.body))
	book.issued = 0
	errors = {}
	try:
		book.save()
	except:
		# TODO: Validation /  Render error in template
		# Cases:
		# 	Duplicate ISBN: django.db.utils.IntegrityError
		#	ISBN: NaN / Length (10, 13)
		#	Year: Invalid
		#	
		errors["error_isbn"] = "Book with the same ISBN already exists in the database."
	return books(request, errors)

def delete(request):
	book = Book.objects.get(isbn=int(json.loads(request.body)["isbn"]))
	if book.issued > 0:
		# TODO: Error delegation
		errors = {"error_delete":"Cannot delete a book that has been issued."}
	else:
		book.delete()
	return books(request)

def edit(request):
	data = json.loads(request.body)
	book = Book.objects.get(isbn=int(data["isbn"]))

	# TODO: Validate
	book.stock = data["stock"]
	book.save()
	return books(request)
from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.core.exceptions import ValidationError

import json

from .forms import BookForm, TransactionForm
from .models import Book, Transaction

def index(request):
	return render(request, "index.html", {
		"book_form":BookForm(),
		"transaction_form":TransactionForm()
	})

def books(request, errors={}):
	# Query the database for list of books
	book_list = serializers.serialize("json", Book.objects.all()[::-1])
	# Return as JSON objects
	print(errors)
	for key in errors:
		if isinstance(errors[key], list):
			errors[key] = " ".join(errors[key])
	return JsonResponse(data={"books":book_list, "errors":errors})

def add(request):
	book = Book(**json.loads(request.body))
	book.issued = 0
	errors = {}
	try:
		book.full_clean()
		book.save()
	except ValidationError as e:
		errors = e.message_dict
	return books(request, errors)

def delete(request):
	book = Book.objects.get(isbn=json.loads(request.body)["isbn"])
	# TODO: Error delegation
	# Invalid ISBN?
	if book.issued > 0:
		errors = {"error_delete":"Cannot delete a book that has been issued."}
	else:
		book.delete()
	return books(request)

def edit(request):
	data = json.loads(request.body)
	book = Book.objects.get(isbn=data["isbn"])
	# TODO: Validate
	# Invalid data*
	# Invalid stock
	# Stock cannot go below issue
	# Dependent fields?
	book.stock = data["stock"]
	book.save()
	return books(request)

def transaction(request):
	errors = {}
	data = json.loads(request.body)
	book = Book.objects.get(isbn=data["isbn"])

	# If no books are in stock and transaction is an issue
	if data["tr"]["transaction_type"] and not book.stock:
		errors["transaction_type"] = "Cannot issue a book that is out-of-stock."
	try:
		transaction = Transaction(book_id=book, **data["tr"])
		transaction.full_clean()
		transaction.save()
	except ValidationError as e:
		errors = {**errors, **e.message_dict}

	# TODO
	# Validate
	# Issue date before return date

	return books(request, errors)





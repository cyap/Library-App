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
	errors = {}
	book = Book(**json.loads(request.body))
	book.issued = 0
	try:
		book.full_clean()
		book.save()
	except ValidationError as e:
		errors = e.message_dict
	return books(request, errors)

def delete(request):
	errors = {}
	book = Book.objects.get(isbn=json.loads(request.body)["isbn"])
	if book.issued > 0:
		errors = {"general":"Cannot delete a book that has been issued."}
	else:
		book.delete()
	return books(request, errors)

def edit(request):
	errors = {}
	data = json.loads(request.body)
	book = Book.objects.get(isbn=data["isbn"])
	try:
		book.stock = data["stock"]
		book.clean()
		book.save()
	except ValidationError as e:
		errors = e.message_dict
	except ValueError:
		errors = {"general":"Invalid stock"}

	return books(request, errors)

def transaction(request):
	errors = {}
	data = json.loads(request.body)
	book = Book.objects.get(isbn=data["isbn"])

	try:
		transaction = Transaction(book_id=book, **data["tr"])
		transaction.full_clean()
		transaction.save()
	except ValidationError as e:
		errors = {**errors, **e.message_dict}

	return books(request, errors)

def get_transactions(request):
	data = json.loads(request.body)
	target_book = Book.objects.get(isbn=data["target"])
	transactions = Transaction.objects.filter(book_id=target_book)
	serialized_transactions = serializers.serialize("json", transactions[::-1])
	return JsonResponse(data={"transactions":serialized_transactions})




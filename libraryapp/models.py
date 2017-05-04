from django.db import models

# Create your models here.
class Book(models.Model):
	title = models.CharField(max_length=255)
	author = models.CharField(max_length=255)
	isbn = models.PositiveIntegerField() 
	stock = models.PositiveIntegerField()
	published = models.IntegerField()
	genre = models.CharField(max_length=255)
	issued = models.PositiveIntegerField()

class Transaction(models.Model):
	book_id = models.ForeignKey(Book, related_name='transactions')
	transaction_type = models.BooleanField()
	transaction_date = models.DateField()
	date = models.DateField()

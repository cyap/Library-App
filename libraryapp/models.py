from django.db import models

# Create your models here.
class Book(models.Model):
	isbn = models.CharField("ISBN Number", max_length=255, unique=True)
	title = models.CharField(max_length=255)
	author = models.CharField(max_length=255)
	published = models.IntegerField("Year Published")
	genre = models.CharField(max_length=255)
	stock = models.PositiveIntegerField()
	issued = models.PositiveIntegerField()

class Transaction(models.Model):
	book_id = models.ForeignKey(Book, related_name='transactions')
	transaction_type = models.BooleanField()
	transaction_date = models.DateField()
	date = models.DateField()

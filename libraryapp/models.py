from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

# Create your models here.
class Book(models.Model):
	isbn = models.CharField("ISBN Number", max_length=255, unique=True)
	title = models.CharField(max_length=255)
	author = models.CharField(max_length=255)
	published = models.IntegerField("Year Published")
	genre = models.CharField(max_length=255)
	stock = models.PositiveIntegerField()
	issued = models.PositiveIntegerField()

	def clean(self):
		error_dict = {}

		# ISBN Validation
		if not (len(self.isbn) == 10 or len(self.isbn) == 13):
			error_dict["isbn"] = _("ISBN must be 10 or 13 digits.")
		try:
			int(self.isbn)
		except:
			error_dict["isbn"] = error_dict.get("isbn", "") + " ISBN must contain numbers only."

		if error_dict:
			raise ValidationError(error_dict)

class Transaction(models.Model):
	book_id = models.ForeignKey(Book, related_name='transactions')
	transaction_type = models.BooleanField("Transaction Type")
	transaction_date = models.DateField("Transaction Date")
	other_date = models.DateField("Issue/Return Date")

	def clean(self):
		error_dict = {}

		if self.transaction_type ^ (self.other_date > self.transaction_date):
			error_dict["transaction_date"] = error_dict.get("transaction_date", "") + "Issue date must precede return date."

		if error_dict:
			raise ValidationError(error_dict)
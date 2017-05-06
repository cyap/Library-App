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

		# Stock
		if self.stock < 0:
			error_dict["stock"] = "Stock must be positive."

		if self.stock < self.issued:
			error_dict["stock"] = error_dict.get("stock", "") + " Stock must be greater than number of books issued."

		# Issued
		if self.issued < 0:
			error_dict["issued"] = "Books issued must be positive."

		if error_dict:
			raise ValidationError(error_dict)

class Transaction(models.Model):
	book_id = models.ForeignKey(Book, related_name='transactions')
	transaction_type = models.BooleanField("Transaction Type")
	transaction_date = models.DateField("Transaction Date")
	other_date = models.DateField("Issue/Return Date")

	def clean(self):
		error_dict = {}

		try:
			if self.transaction_type ^ (self.other_date > self.transaction_date):
				error_dict["transaction_date"] = "Issue date must precede return date."
		except:
			pass

		if self.transaction_type:
			# If no books are in stock and transaction is an issue
			if not self.book_id.stock:
				error_dict["transaction_type"] = "Cannot issue a book that is out-of-stock."
			else:
				self.book_id.issued += 1

		else:
			# If transaction is a return
			self.book_id.issued -= 1

		# Validate transaction on book
		try:
			self.book_id.clean()
		except ValidationError as e:
			error_dict["transaction_type"] = " ".join([error_dict.get("transaction_type", ""), "".join(*(e.message_dict.values()))])
		
		if error_dict:
			raise ValidationError(error_dict)
		else:
			self.book_id.save()



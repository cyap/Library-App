from django import forms
from django.utils.safestring import mark_safe

from .models import Book, Transaction
from .widgets import CustomDateWidget


class InlineRender(forms.RadioSelect.renderer):
	def render(self):
		return mark_safe(" ".join([str(self[0]), str(self[1])]))

class BookForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(BookForm, self).__init__(*args, **kwargs)
		# Add custom "ng-model" attribute to each field rendered by the form
		for field_name, field_object in self.fields.items():
			field_object.widget.attrs.update({"ng-model":"book."+field_name})

	class Meta:
		model = Book
		fields = ["title", "author", "isbn", "stock", "published", "genre"]

class TransactionForm(forms.ModelForm):

	def __init__(self, *args, **kwargs):
		super(TransactionForm, self).__init__(*args, **kwargs)
		# Add custom "ng-model" attribute to each field rendered by the form
		for field_name, field_object in self.fields.items():
			field_object.widget.attrs.update({"ng-model":"tr."+field_name})

	class Meta:
		YEARS = [year for year in range(2000,2010)]
		model = Transaction
		fields = ["transaction_type", "transaction_date", "other_date"]
		# Override default renderer for inline radio buttons
		widgets = {
					"transaction_type": forms.RadioSelect(
							renderer=InlineRender, 
							choices=[(True,"Issue"), (False,"Return")]),
					"transaction_date": CustomDateWidget(years = YEARS),
					"other_date": CustomDateWidget(years = YEARS)

		}


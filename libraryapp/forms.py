from django import forms

from .models import Book, Transaction

class BookForm(forms.ModelForm):

	def __init__(self, *args, **kwargs):
		super(BookForm, self).__init__(*args, **kwargs)
		# Add custom "ng-model" attribute to each field rendered by the form
		for field_name, field_object in self.fields.items():
			field_object.widget.attrs.update({"ng-model":field_name})

	class Meta:
		model = Book
		fields = ["title", "author", "isbn", "stock", "published", "genre"]
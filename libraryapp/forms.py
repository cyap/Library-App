from django import forms

class BookForm(forms.Form):
	title = forms.CharField(label="Title")
	author = forms.CharField(label="Author")
	isbn = forms.IntegerField(label="ISBN Number") 
	stock = forms.IntegerField(label="Stock")
	published = forms.IntegerField(label="Publication Year")
	genre = forms.IntegerField(label="Genre")
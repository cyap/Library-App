from django.forms.widgets import Widget, SelectDateWidget

class CustomDateWidget(SelectDateWidget):

	""" 
		Hacky solution for overriding Django's default date-picker form such 
		that uniquely named ng-directives can be included in each input tag. 
		The date-picker widget includes three input fields, and any attrs that
		are assigned to the SelectDateWidget are applied to all three fields, 
		meaning they each share the same ng-model.

		A cleanear solution would be to override the base widget's 
		get_context method, which handles the constructor data before converting 
		it into HTML. For reasons unbeknowst to me currently, it is
		inaccessible, so I have elected to instead directly modify the HTML 
		before it is rendered.

	"""
	
	def __init__(self, attrs=None, years=None, months=None, empty_label=None, test=None):
		super(CustomDateWidget, self).__init__(attrs, years, months, empty_label)
		print(dir(self))
		print(self.attrs)

	def render(self, name, value, attrs=None):
		print(name)
		context = super().render(name, value, attrs=attrs)
		context_args = context.split('"tr.{0}"'.format(name))
		new_context = '{1}{0}_month{2}{0}_day{3}{0}_year{4}'.format(name, *context_args)
		return new_context
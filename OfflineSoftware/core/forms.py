from django import forms
from .models import Project
from .models import Material
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms



class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'number']



class ExcelImportForm(forms.Form):
    excel_file = forms.FileField()


class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['name', 'quantity', 'unit_price']

class ExcelImportForm(forms.Form):
    excel_file = forms.FileField()




# core/forms.py


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# core/forms.py

from django import forms
from .models import Material

class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['name', 'quantity', 'unit_price']

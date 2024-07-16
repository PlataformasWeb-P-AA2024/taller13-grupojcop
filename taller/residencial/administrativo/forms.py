from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from django import forms

from administrativo.models import Edificio, \
        Departamento

class EdificioForm(ModelForm):
    
    class Meta:
        model = Edificio
        fields = ['nombre', 'direccion', 'ciudad', 'tipo']
        labels = {
            'nombre': _('Ingrese nombre por favor'),
            'direccion': _('Ingrese dirección por favor'),
            'ciudad': _('Ingrese ciudad por favor'),
            'tipo': _('Ingrese tipo por favor'),
        }

    def clean_ciudad(self):
        valor = self.cleaned_data['ciudad']
        if valor.startswith('L'):
            raise forms.ValidationError("El nombre de la ciudad no puede comenzar con la letra mayúscula L")
        return valor

class DepartamentoForm(ModelForm):

    class Meta:
        model = Departamento
        fields = ['nombre_completo_propietario', 'costo_departamento', 'numero_cuartos',  'edificio']
        labels = {
            'nombre_completo_propietario': _('Ingrese nombre completo del propietario por favor'),
            'costo_departamento': _('Ingrese el costo del departamento por favor'),
            'numero_cuartos': _('Ingrese el número de cuartos por favor'),
            'edificio': _('Ingrese el edificio por favor'),
        }

    def clean_nombre_completo_propietario(self):
        valor = self.cleaned_data['nombre_completo_propietario']
        if len(valor.split()) < 3:
            raise forms.ValidationError("El nombre completo del propietario no debe tener menos de tres palabras")
        return valor
    
    def clean_costo_departamento(self):
        valor = self.cleaned_data['costo_departamento']
        if valor > 100000:
            raise forms.ValidationError("El costo del departamento no puede ser mayor a 100 mil")
        return valor
    
    def clean_numero_cuartos(self):
        valor = self.cleaned_data['numero_cuartos']
        if valor <= 0 or valor > 7:
            raise forms.ValidationError("El número de cuartos no puede ser 0 ni mayor a 7")
        return valor



class DepartamentoEdificioForm(ModelForm):

    def __init__(self, edificio, *args, **kwargs):
        super(DepartamentoEdificioForm, self).__init__(*args, **kwargs)
        self.initial['edificio'] = edificio
        self.fields["edificio"].widget = forms.widgets.HiddenInput()
        print(edificio)

    class Meta:
        model = Departamento
        fields = ['nombre_completo_propietario', 'costo_departamento', 'numero_cuartos',  'edificio']
        labels = {
            'nombre_completo_propietario': _('Ingrese nombre completo del propietario por favor'),
            'costo_departamento': _('Ingrese el costo del departamento por favor'),
            'numero_cuartos': _('Ingrese el número de cuartos por favor'),
            'edificio': _('Ingrese el edificio por favor'),
        }

    def clean_nombre_completo_propietario(self):
            valor = self.cleaned_data['nombre_completo_propietario']
            if len(valor.split()) < 3:
                raise forms.ValidationError("El nombre completo del propietario no debe tener menos de tres palabras")
            return valor
        
    def clean_costo_departamento(self):
        valor = self.cleaned_data['costo_departamento']
        if valor > 100000:
            raise forms.ValidationError("El costo del departamento no puede ser mayor a 100 mil")
        return valor
        
    def clean_numero_cuartos(self):
        valor = self.cleaned_data['numero_cuartos']
        if valor <= 0 or valor > 7:
            raise forms.ValidationError("El número de cuartos no puede ser 0 ni mayor a 7")
        return valor
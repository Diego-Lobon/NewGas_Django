from django.forms import *
from venta.models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


    




class mensajeContactoForm(ModelForm):
    
    class Meta:
        
        model = mensajeContacto
        fields = ['nombre', 'apellido', 'correoElectronico', 'empresa', 'celular', 'dni', 'consulta']
        labels = {
            'nombre': '',
            'apellido': '',
            'correoElectronico': '',
            'empresa': '',
            'celular': '',
            'consulta': '',
            'dni': ''
        }
        widgets = {
            'nombre': TextInput(
                attrs={
                    'class': 'input_form input_nombre',
                    'placeholder': 'Nombre'
                }
            ),
            'apellido': TextInput(
                attrs={
                    'class': 'input_form input_apellido',
                    'placeholder': 'Apellido'
                }
            ),
            'correoElectronico': TextInput(
                attrs={
                    'class': 'input_form input_correo',
                    'placeholder': 'Correo Electronico'
                }
            ),
            'empresa': TextInput(
                attrs={
                    'class': 'input_form input_empresa',
                    'placeholder': 'Empresa'
                }
            ),
            'celular': TextInput(
                attrs={
                    'class': 'input_form input_celular',
                    'placeholder': 'Celular'
                }
            ),
            'consulta': Textarea(
                attrs={
                    'class': 'input_form input_consulta',
                    'placeholder': 'Consulta'
                }
            ),
            'dni': TextInput(
                attrs={
                    'class': 'input_form input_dni',
                    'placeholder': 'Nro. de DNI'
                }
            )
        }

    



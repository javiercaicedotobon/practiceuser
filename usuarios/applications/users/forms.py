from django import forms
from .models import User

from django.contrib.auth import authenticate


class UserForm(forms.ModelForm):
    
    password1 = forms.CharField(
        label = 'Contraseña',
        required = True,
        widget = forms.PasswordInput(
            attrs={'placeholder':'Ingrese Contraseña'}
        )
    )
    
    password2 = forms.CharField(
        label = 'Contraseña',
        required = True,
        widget = forms.PasswordInput(
            attrs={'placeholder':'Repita Contraseña'}
        )
    )
    
    
    
    class Meta:
        model = User
        fields = (
            'username',
            'nombres',
            'apellidos',
            'email',
            'genero'
        )
    
    
    def clean_password2(self):
        if self.cleaned_data['password2'] != self.cleaned_data['password1']:
            self.add_error('password2', 'Las contraseñas no coinciden')



class LoginForm(forms.Form):
    
    username = forms.CharField(
        label = 'Usuario',
        required = True,
        widget = forms.TextInput(
            attrs = {'placeholder':'Ingrese usuario'}
        )
    )
    
    password = forms.CharField(
        label = 'Contraseña',
        required = True,
        widget = forms.PasswordInput(
            attrs = {'placeholder':'Ingrese contraseña'}
        )
    )
    


    def clean(self):
        
        cleaned_data = super(LoginForm, self).clean()
        
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        
        if not authenticate(username=username, password=password):
            raise forms.ValidationError('Usuario o Contraseña incorrecta')
            
        return self.cleaned_data



class UpdatePasswordForm(forms.Form):
    
    password1 = forms.CharField(
        label='Contraseña Actual',
        required=True,
        widget=forms.PasswordInput(
            attrs={'placeholder':'Contraseña Actual'}
        )
    )
    
    
    password2 = forms.CharField(
        label='Nueva Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={'placeholder':'Nueva Contraseña'}
        )
    )



class VerificationForm(forms.Form):
    codregistro = forms.CharField(required=True)
    
    
    
    def __init__(self, pk, *args, **kwargs):
        self.id_user = pk
        super(VerificationForm, self).__init__(*args, **kwargs)
    
    
    def clean_codregistro(self):
        codigo = self.cleaned_data['codregistro']
        
        if len(codigo) == 6:
            #verificamos si el codigo y el id son validos
            activo = User.objects.cod_validation(
                self.id_user,
                codigo
            )
            if not activo:
                raise forms.ValidationError('El codigo es incorrecto')
        else:
            raise forms.ValidationError('El codigo es incorrecto')
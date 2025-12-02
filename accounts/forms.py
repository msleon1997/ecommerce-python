from django import forms
from .models import Account

class RegistrationForm(forms.ModelForm):
   password = forms.CharField(widget=forms.PasswordInput(attrs={
       'placeholder': 'Ingrese su contraseña',
       'class': 'form-control'
    }))
   
   confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
       'placeholder': 'Repita la contraseña',
       'class': 'form-control'
    }))
   
       
   class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'phone', 'mail', 'password']

   def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Ingrese sus nombres'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Ingrese sus apellidos'
        self.fields['phone'].widget.attrs['placeholder'] = 'Ingrese su número de teléfono o celular'
        self.fields['mail'].widget.attrs['placeholder'] = 'Ingrese su correo electrónico'
        
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            
   def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password != confirm_password:
            raise forms.ValidationError(
                "Las contraseñas no coinciden"
            )
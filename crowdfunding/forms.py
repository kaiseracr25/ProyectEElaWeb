from django import forms
from django.utils import timezone
from .models import Donation, Campaign, Category

# 1. FORMULARIO DE DONACIÓN
class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['monto', 'comentario']
        widgets = {
            'monto': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 50.00', 'min': '1'}),
            'comentario': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Un mensaje de apoyo...'}),
        }

    # Validación personalizada: El monto debe ser mayor a 0
    def clean_monto(self):
        monto = self.cleaned_data.get('monto')
        if monto is not None and monto <= 0:
            raise forms.ValidationError("El monto de la donación debe ser positivo.")
        return monto


# 2. FORMULARIO DE CAMPAÑA
class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = ['titulo', 'descripcion', 'categoria', 'monto_objetivo', 'fecha_inicio', 'fecha_fin', 'imagen']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'monto_objetivo': forms.NumberInput(attrs={'class': 'form-control'}),
            
            # --- CONFIGURACIÓN DE FECHA DE INICIO ---
            # 'type': 'date' -> Muestra el calendario.
            # 'readonly': 'readonly' -> Impide que el usuario cambie la fecha manualmente.
            'fecha_inicio': forms.DateInput(attrs={
                'class': 'form-control', 
                'type': 'date', 
                'readonly': 'readonly' 
            }),
            
            'fecha_fin': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'imagen': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(CampaignForm, self).__init__(*args, **kwargs)
        # Si estamos creando una nueva campaña (no tiene ID todavía),
        # forzamos la fecha de inicio a "hoy".
        if not self.instance.pk:
            self.fields['fecha_inicio'].initial = timezone.now().date()


# 3. FORMULARIO DE CATEGORÍA
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
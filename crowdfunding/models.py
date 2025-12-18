from django.db import models
from django.contrib.auth.models import User # Importamos el usuario nativo de Django

# 1. Modelo de Categoría 
class Category(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

# 2. Modelo de Campaña 
class Campaign(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    # Relación: Una campaña pertenece a una categoría 
    categoria = models.ForeignKey(Category, on_delete=models.CASCADE)
    monto_objetivo = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    activa = models.BooleanField(default=True)
    # Imagen opcional ( Pillow) 
    imagen = models.ImageField(upload_to='campanas/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo
    
    # Opcional: Método helper para calcular lo recaudado 
    def monto_recaudado(self):
        # Sumamos todas las donaciones asociadas a esta campaña
        total = self.donation_set.aggregate(models.Sum('monto'))['monto__sum']
        return total if total else 0

# 3. Modelo de Donación 
class Donation(models.Model):
    # Relación: Usuario que dona 
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    # Relación: Campaña a la que se dona [
    campanha = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    comentario = models.TextField(null=True, blank=True) # Opcional 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Donación de {self.monto} a {self.campanha.titulo}"
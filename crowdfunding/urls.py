from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('campana/<int:campana_id>/', views.detalle_campana, name='detalle_campana'),
    path('mis-donaciones/', views.mis_donaciones, name='mis_donaciones'),
    path('registro/', views.registro, name='registro'),
    
    # Gestión de Campañas
    path('campana/nueva/', views.crear_campana, name='crear_campana'),
    path('campana/editar/<int:campana_id>/', views.editar_campana, name='editar_campana'),
    path('campana/eliminar/<int:campana_id>/', views.eliminar_campana, name='eliminar_campana'),

    # Gestión de Categorías
    path('categorias/', views.lista_categorias, name='lista_categorias'),
    path('categorias/nueva/', views.crear_categoria, name='crear_categoria'),
    path('categorias/editar/<int:category_id>/', views.editar_categoria, name='editar_categoria'),
    path('categorias/eliminar/<int:category_id>/', views.eliminar_categoria, name='eliminar_categoria'),
]
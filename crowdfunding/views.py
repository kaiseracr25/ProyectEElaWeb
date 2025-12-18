from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.db.models import Sum
from .models import Campaign, Donation, Category
from .forms import DonationForm, CampaignForm, CategoryForm

def es_admin(user):
    return user.is_superuser

# (Puntos 4 y 5) Modificación del Index
def index(request):
    # Obtener el ID de la categoría del filtro (si existe)
    categoria_id = request.GET.get('categoria')
    
    # Ordenar: Primero las Activas (-activa), luego las más recientes (-fecha_inicio)
    campanas = Campaign.objects.all().order_by('-activa', '-fecha_inicio')

    # Filtrar por categoría si se seleccionó una
    if categoria_id:
        campanas = campanas.filter(categoria_id=categoria_id)

    # Necesitamos las categorías para pintar el menú de filtros
    categorias = Category.objects.all()

    return render(request, 'crowdfunding/index.html', {
        'campanas': campanas, 
        'categorias': categorias, # Pasamos las categorías al template
        'categoria_seleccionada': int(categoria_id) if categoria_id else None
    })

def detalle_campana(request, campana_id):
    campana = get_object_or_404(Campaign, pk=campana_id)
    total_recaudado = campana.donation_set.aggregate(Sum('monto'))['monto__sum'] or 0
    
    # Evitar división por cero si la meta es 0 (caso borde)
    if campana.monto_objetivo > 0:
        porcentaje = (total_recaudado / campana.monto_objetivo) * 100
    else:
        porcentaje = 0
    
    if request.method == 'POST':
        # (Punto 6) Validación extra: Admin no puede donar
        if request.user.is_superuser:
            return redirect('detalle_campana', campana_id=campana.id)

        if not request.user.is_authenticated:
             return redirect(f'/accounts/login/?next={request.path}')

        form = DonationForm(request.POST)
        if form.is_valid():
            donacion = form.save(commit=False)
            donacion.usuario = request.user
            donacion.campanha = campana
            donacion.save()
            return redirect('detalle_campana', campana_id=campana.id)
    else:
        form = DonationForm()

    donaciones = campana.donation_set.all().order_by('-created_at')

    return render(request, 'crowdfunding/detalle.html', {
        'campana': campana,
        'total_recaudado': total_recaudado,
        'porcentaje': min(porcentaje, 100),
        'form': form,
        'donaciones': donaciones
    })

@login_required
def mis_donaciones(request):
    donaciones = Donation.objects.filter(usuario=request.user).order_by('-created_at')
    total_donado = donaciones.aggregate(Sum('monto'))['monto__sum'] or 0

    return render(request, 'crowdfunding/mis_donaciones.html', {
        'donaciones': donaciones,
        'total_donado': total_donado
    })

def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'crowdfunding/registro.html', {'form': form})

# --- GESTIÓN DE CAMPAÑAS ---

@user_passes_test(es_admin)
def crear_campana(request):
    if request.method == 'POST':
        form = CampaignForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = CampaignForm()
    return render(request, 'crowdfunding/crear_campana.html', {'form': form})

@user_passes_test(es_admin)
def editar_campana(request, campana_id):
    campana = get_object_or_404(Campaign, pk=campana_id)
    if request.method == 'POST':
        form = CampaignForm(request.POST, request.FILES, instance=campana)
        if form.is_valid():
            form.save()
            return redirect('detalle_campana', campana_id=campana.id)
    else:
        form = CampaignForm(instance=campana)
    return render(request, 'crowdfunding/crear_campana.html', {'form': form, 'titulo': 'Editar Campaña'})

# (Punto 3) Eliminación Lógica (Cerrar Campaña)
@user_passes_test(es_admin)
def eliminar_campana(request, campana_id):
    campana = get_object_or_404(Campaign, pk=campana_id)
    
    if request.method == 'POST':
        # En lugar de .delete(), cambiamos el estado a Inactiva
        campana.activa = False
        campana.save()
        return redirect('index')
    
    # Reutilizamos el template pero cambiamos el texto para que diga "Cerrar" en lugar de "Eliminar"
    return render(request, 'crowdfunding/confirmar_eliminar.html', {
        'objeto': campana.titulo, 
        'tipo': 'Campaña (Pasará a estado CERRADA)',
        'accion_texto': 'Sí, Cerrar Campaña' # Variable opcional para el botón
    })

# --- GESTIÓN DE CATEGORÍAS ---

@user_passes_test(es_admin)
def lista_categorias(request):
    categorias = Category.objects.all()
    return render(request, 'crowdfunding/lista_categorias.html', {'categorias': categorias})

@user_passes_test(es_admin)
def crear_categoria(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_categorias')
    else:
        form = CategoryForm()
    return render(request, 'crowdfunding/form_categoria.html', {'form': form, 'titulo': 'Nueva Categoría'})

@user_passes_test(es_admin)
def editar_categoria(request, category_id):
    categoria = get_object_or_404(Category, pk=category_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            return redirect('lista_categorias')
    else:
        form = CategoryForm(instance=categoria)
    return render(request, 'crowdfunding/form_categoria.html', {'form': form, 'titulo': 'Editar Categoría'})

# (Punto 2) Validación al eliminar Categoría
@user_passes_test(es_admin)
def eliminar_categoria(request, category_id):
    categoria = get_object_or_404(Category, pk=category_id)
    
    # Validamos si existen campañas activas asociadas a esta categoría
    if categoria.campaign_set.filter(activa=True).exists():
        # Si existen, no permitimos borrar y mostramos error (podríamos hacer una página de error, 
        # pero para ser prácticos, reutilizamos confirmar_eliminar con un flag de error)
        return render(request, 'crowdfunding/confirmar_eliminar.html', {
            'objeto': categoria.nombre,
            'tipo': 'Categoría',
            'error': 'No se puede eliminar esta categoría porque tiene campañas activas asociadas.'
        })

    if request.method == 'POST':
        categoria.delete()
        return redirect('lista_categorias')
        
    return render(request, 'crowdfunding/confirmar_eliminar.html', {'objeto': categoria.nombre, 'tipo': 'Categoría'})
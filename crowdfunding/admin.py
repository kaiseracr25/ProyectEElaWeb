from django.contrib import admin
from .models import Category, Campaign, Donation

# Registramos los modelos para que aparezcan en el panel
admin.site.register(Category)
admin.site.register(Campaign)
admin.site.register(Donation)
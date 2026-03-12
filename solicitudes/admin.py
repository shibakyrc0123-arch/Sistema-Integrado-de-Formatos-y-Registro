from django.contrib import admin

# Register your models here.


# Comentario: Importamos el módulo de administración de Django.
from django.contrib import admin
# Comentario: Importamos tus modelos desde el archivo local.
from .models import RequisicionInterna, DiccionarioItems

# Comentario: Registramos los modelos para que sean visibles en el panel /admin.
admin.site.register(RequisicionInterna)
admin.site.register(DiccionarioItems)

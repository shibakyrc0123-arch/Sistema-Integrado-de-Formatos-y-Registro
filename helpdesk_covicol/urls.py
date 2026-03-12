# =========================================================================
# 🗺️ DICCIONARIO MAESTRO DE RUTAS: helpdesk_covicol/urls.py
# =========================================================================

# Comentario: Importamos el panel de administración.
from django.contrib import admin
# Comentario: Importamos 'path' e 'include'. 'include' es VITAL aquí.
from django.urls import path, include
from django.shortcuts import render

urlpatterns = [
    # Comentario: Ruta para el panel de administración.
    path('admin/', admin.site.urls),
    
    # Comentario: Aquí le decimos al proyecto que todas las rutas que
    # empiecen con 'solicitud/' se manejen en el archivo que acabamos de crear.
    path('', include('solicitudes.urls')),
    
]

